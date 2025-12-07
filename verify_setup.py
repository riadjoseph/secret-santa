import os
import resend
from supabase import create_client, Client
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

def test_supabase():
    print("Testing Supabase connection...")
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_ANON_KEY")
    
    if not url or not key:
        print("❌ Supabase credentials missing in .env")
        return False
        
    try:
        supabase: Client = create_client(url, key)
        print("✅ Supabase client initialized")
        
        # Check for all required tables
        required_tables = ["participants", "sponsors", "sponsor_gifts", "assignments", "disputes"]
        all_tables_ok = True
        
        for table in required_tables:
            try:
                # Using count to be safe and verify existence
                response = supabase.table(table).select("count", count="exact").execute()
                print(f"✅ Table '{table}' exists. Count: {response.count}")
            except Exception as e:
                print(f"❌ Table '{table}' check FAILED. Error: {e}")
                all_tables_ok = False

        return all_tables_ok
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return False

def test_resend():
    print("\nTesting Resend configuration...")
    api_key = os.environ.get("RESEND_API_KEY")
    
    if not api_key:
        print("❌ Resend API Key missing in .env")
        return False
        
    resend.api_key = api_key
    if api_key.startswith("re_"):
        print("✅ Resend API Key format looks correct")
        return True
    else:
        print("❌ Resend API Key format invalid")
        return False

if __name__ == "__main__":
    print("--- Verification Start ---")
    
    supabase_ok = test_supabase()
    resend_ok = test_resend()
    
    if supabase_ok and resend_ok:
        print("\n✅ Full infrastructure verification PASSED")
    else:
        print("\n❌ Verification FAILED or INCOMPLETE")
        sys.exit(1)
