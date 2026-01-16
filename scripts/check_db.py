import os
import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

load_dotenv()

# Get config from env
DB_USER = os.getenv("POSTGRES_USER", "langgraph_user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "secure_password")
DB_HOST = "localhost"
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "langgraph_db")

DB_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def check_db():
    print(f"Connecting to {DB_URL.replace(DB_PASS, '***')}...")
    engine = create_engine(DB_URL)
    
    # Retry logic
    for i in range(5):
        try:
            with engine.connect() as conn:
                print("Connection successful!")
                
                # Check extensions
                result = conn.execute(text("SELECT extname FROM pg_extension;"))
                extensions = [row[0] for row in result]
                print(f"Installed extensions: {extensions}")
                
                if "vector" not in extensions:
                    print("❌ ERROR: 'vector' extension is MISSING!")
                else:
                    print("✅ 'vector' extension is present.")
                
                # Check tables
                result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"))
                tables = [row[0] for row in result]
                print(f"Existing tables: {tables}")
                
                return
        except OperationalError as e:
            print(f"Connection failed (attempt {i+1}/5): {str(e)}")
            time.sleep(2)
            
    print("❌ Failed to connect to database.")

if __name__ == "__main__":
    check_db()