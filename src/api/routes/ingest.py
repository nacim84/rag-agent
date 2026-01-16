from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
import tempfile
import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector
from src.api.auth import get_current_client
from src.rag.embeddings import get_embeddings
from src.config.settings import settings
from src.config.database import engine # Import shared AsyncEngine
from src.api.schemas import ChatResponse 

router = APIRouter()

@router.post("/ingest")
async def ingest_document(
    file: UploadFile = File(...),
    domain: str = Form(..., pattern="^(comptable|transaction|exploitation)$"),
    client_id: str = Depends(get_current_client)
):
    """
    Ingest a document (PDF or Text) into the client's vector store.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is missing")

    # 1. Save to temp file to use Loaders
    suffix = os.path.splitext(file.filename)[1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        # 2. Load Document
        docs = []
        if suffix == ".pdf":
            loader = PyPDFLoader(tmp_path)
            docs = await loader.aload()
        elif suffix in [".txt", ".md", ".csv"]:
            loader = TextLoader(tmp_path, encoding="utf-8")
            # TextLoader is sync usually, but we can run it
            docs = loader.load()
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
            
        if not docs:
            raise HTTPException(status_code=400, detail="Empty document")

        # 3. Add Metadata
        for doc in docs:
            doc.metadata["source"] = file.filename
            doc.metadata["client_id"] = client_id
            doc.metadata["domain"] = domain

        # 4. Chunk Document
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(docs)

        # 5. Store in Vector DB
        table_name = f"documents_{domain}_{client_id}"
        embeddings = get_embeddings()
        
        # Initialize PGVector with shared AsyncEngine
        # This helps reuse the connection pool and context
        vector_store = PGVector(
            embeddings=embeddings,
            collection_name=table_name,
            connection=engine,
            use_jsonb=True,
            create_extension=False, # We handle extension creation in init_db.sql
        )
        
        # Add documents (async)
        await vector_store.aadd_documents(splits)

        return {
            "status": "success",
            "filename": file.filename,
            "chunks": len(splits),
            "table": table_name
        }

    except Exception as e:
        # Log the full error traceback for debugging
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # Cleanup temp file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)