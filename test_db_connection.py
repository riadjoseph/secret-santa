"""
Test script to verify Supabase connection and data
"""
import os
from dotenv import load_dotenv
from utils.db import get_supabase_client, get_all_participants

load_dotenv()

# Test Supabase connection
print("Testing Supabase connection...")
print(f"SUPABASE_URL: {os.getenv('SUPABASE_URL')[:30]}..." if os.getenv('SUPABASE_URL') else "SUPABASE_URL: Not set")
print(f"SUPABASE_SERVICE_ROLE_KEY: {'Set' if os.getenv('SUPABASE_SERVICE_ROLE_KEY') else 'Not set'}")

# Try to get client
try:
    # Mock streamlit for testing
    class MockSecrets:
        def get(self, key):
            return os.getenv(key)

    class MockSt:
        secrets = MockSecrets()

    import sys
    sys.modules['streamlit'] = MockSt()

    from supabase import create_client

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if url and key:
        client = create_client(url, key)
        print("✅ Supabase client created successfully!")

        # Test fetching participants
        print("\nFetching participants...")
        response = client.table("participants").select("*").execute()
        print(f"Found {len(response.data)} participants")

        if response.data:
            print("\nParticipants:")
            for p in response.data:
                print(f"  - {p.get('name')} ({p.get('email')}) - {p.get('expertise_level')}")
        else:
            print("  No participants found. Register some users first!")

        # Test fetching assignments
        print("\nFetching assignments...")
        response = client.table("assignments").select("*").execute()
        print(f"Found {len(response.data)} assignments")

    else:
        print("❌ Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
