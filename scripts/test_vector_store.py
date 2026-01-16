import os
from sqlalchemy import create_engine, text
from pgvector.sqlalchemy import Vector
from dotenv import load_dotenv
import numpy as np

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER", "langgraph_user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "secure_password")
DB_HOST = "localhost"
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "langgraph_db")

DB_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def test_vector_operations():
    print("Testing PGVector operations...")
    engine = create_engine(DB_URL)
    
    with engine.connect() as conn:
        # 1. Create test table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS test_vectors (
                id SERIAL PRIMARY KEY,
                content TEXT,
                embedding vector(3) 
            );
        """))
        print("✅ Test table created.")
        
        # 2. Insert dummy vector
        # Using 3 dimensions for simplicity (Gemini is 768, but this is just a test)
        vec = [0.1, 0.2, 0.3]
        conn.execute(
            text("INSERT INTO test_vectors (content, embedding) VALUES (:c, :e)"),
            {"c": "Test Document", "e": str(vec)}
        )
        conn.commit()
        print("✅ Vector inserted.")
        
        # 3. Query similar vector
        # L2 distance operator <->
        result = conn.execute(text("""
            SELECT content, embedding <-> '[0.1, 0.2, 0.3]' as distance 
            FROM test_vectors 
            ORDER BY distance ASC 
            LIMIT 1;
        """))
        row = result.fetchone()
        print(f"✅ Query result: Content='{row[0]}', Distance={row[1]}")
        
        # Cleanup
        conn.execute(text("DROP TABLE test_vectors;"))
        conn.commit()
        print("✅ Cleanup done.")

if __name__ == "__main__":
    test_vector_operations()
