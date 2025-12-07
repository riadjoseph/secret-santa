import os
import streamlit as st
from supabase import create_client, Client

# Initialize Supabase Client
@st.cache_resource
def get_supabase_client():
    url = None
    key = None
    
    # Try secrets (Streamlit Cloud)
    try:
        if hasattr(st, "secrets"):
            url = st.secrets.get("SUPABASE_URL")
            key = st.secrets.get("SUPABASE_SERVICE_ROLE_KEY")
    except Exception:
        pass
        
    # Fallback to env (Local/Script)
    if not url: url = os.getenv("SUPABASE_URL")
    if not key: key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
    
    if not url or not key:
        return None
    return create_client(url, key)

supabase = get_supabase_client()

def load_user_profile(email):
    """Load user profile from Supabase."""
    if not supabase: return None
    try:
        response = supabase.table("participants").select("*").eq("email", email).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error loading profile: {e}")
        return None

def save_profile(email, data):
    """Upsert user profile."""
    if not supabase:
        print("Error: Supabase client not initialized")
        return False, "Database connection not available"

    try:
        payload = {
            "email": email,
            "name": data["name"],
            "linkedin_url": data["linkedin_url"],
            "website_url": data["website_url"],
            "bio": data["bio"],
            "address": data.get("address", ""),
            "pledge": data["pledge"],
            "expertise_level": data["expertise_level"],
            "wishlist": data["wishlist"]
        }

        existing = load_user_profile(email)
        if existing:
            response = supabase.table("participants").update(payload).eq("email", email).execute()
        else:
            response = supabase.table("participants").insert(payload).execute()

        return True, "Profile saved successfully"
    except Exception as e:
        error_msg = str(e)
        print(f"Error saving profile: {error_msg}")
        return False, f"Failed to save profile: {error_msg}"

def get_all_participants():
    """Fetch all participants for matching."""
    if not supabase: return []
    try:
        response = supabase.table("participants").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error fetching participants: {e}")
        return []

def save_assignments(assignments):
    """Save generated assignments to DB.
    assignments: list of dicts {'giver_email': x, 'receiver_email': y}
    """
    if not supabase: return False
    try:
        # We don't delete immediately to be safe, but typically we'd clear old ones for a new run

        data = []
        for giver, receiver in assignments.items():
            data.append({
                "giver_email": giver,
                "receiver_email": receiver,
                "status": "pending"
            })

        if data:
            supabase.table("assignments").insert(data).execute()
        return True
    except Exception as e:
        print(f"Error saving assignments: {e}")
        return False

def get_all_assignments():
    """Fetch all assignments from DB."""
    if not supabase: return []
    try:
        response = supabase.table("assignments").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error fetching assignments: {e}")
        return []

def get_assignment_for_user(email):
    """Get the assignment for a specific user (who they should give to)."""
    if not supabase: return None
    try:
        response = supabase.table("assignments").select("*").eq("giver_email", email).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error fetching assignment: {e}")
        return None
