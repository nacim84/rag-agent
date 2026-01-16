import os
import sys
from dotenv import load_dotenv

# Load env
load_dotenv()

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.tools.google.drive import drive_client
from src.config.settings import settings

def test_drive():
    print("🚗 Testing Google Drive Integration...")
    
    print(f"🔑 Checking credentials path: {settings.GOOGLE_SERVICE_ACCOUNT_PATH}")
    
    if not drive_client.service:
        print("❌ Service not initialized. Check credentials.")
        return

    print("✅ Service initialized.")
    
    print("\n📂 Listing first 5 files...")
    files = drive_client.list_files(page_size=5)
    
    if not files:
        print("⚠️ No files found (or empty Drive).")
    else:
        for f in files:
            print(f"   - [{f['mimeType']}] {f['name']} (ID: {f['id']})")
            
    print("\n✅ Test Complete.")

if __name__ == "__main__":
    test_drive()
