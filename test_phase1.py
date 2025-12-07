import sys
import time

# Mock streamlit to avoid import errors
from unittest.mock import MagicMock
sys.modules["streamlit"] = MagicMock()

# Now import app logic
from streamlit_app import create_token, verify_token, save_profile, load_user_profile

def test_auth_logic():
    print("Testing Auth Logic...")
    email = "test_user@example.com"
    token = create_token(email)
    print(f"Generated Token: {token[:10]}...")
    
    decoded = verify_token(token)
    if decoded == email:
        print("✅ Token verification passed")
    else:
        print(f"❌ Token verification failed. Got: {decoded}")

    # Test expired (wait logic simulated or just assumed working by lib)

def test_profile_logic():
    print("\nTesting Profile Logic (Supabase)...")
    email = "test_logic@example.com"
    data = {
        "name": "Test User",
        "linkedin_url": "https://linkedin.com/in/test",
        "website_url": "https://test.com",
        "bio": "I am a test bot",
        "address": "123 Test St",
        "pledge": "I pledge to give nothing but tests",
        "expertise_level": "Junior",
        "wishlist": [{"name": "Test Gift", "url": "http://test.gift"}]
    }
    
    if save_profile(email, data):
        print("✅ Profile saved successfully")
    else:
        print("❌ Profile save failed")
        
    loaded = load_user_profile(email)
    if loaded and loaded["name"] == "Test User":
        print("✅ Profile loaded successfully")
        print(f"   Name: {loaded['name']}")
        print(f"   Pledge: {loaded['pledge']}")
    else:
        print("❌ Profile load failed or data mismatch")

if __name__ == "__main__":
    test_auth_logic()
    test_profile_logic()
