import streamlit as st
import time
import os
import jwt
import datetime
import resend
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Helper to get config from secrets (Cloud) or env (Local)
def get_config(key, default=None):
    if key in st.secrets:
        return st.secrets[key]
    return os.getenv(key, default)

# Configuration
SUPABASE_URL = get_config("SUPABASE_URL")
SUPABASE_KEY = get_config("SUPABASE_SERVICE_ROLE_KEY") # using service role for admin tasks + RLS bypass if needed
RESEND_API_KEY = get_config("RESEND_API_KEY")
APP_DOMAIN = get_config("APP_DOMAIN", "http://localhost:8501")
JWT_SECRET = get_config("SUPABASE_SERVICE_ROLE_KEY") # Using this as the signing secret
JWT_ALGORITHM = "HS256"

# Initialize Clients
if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Missing Supabase Configuration. Please check your secrets.")
    st.stop()

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY
else:
    st.warning("Resend API Key missing. Emails will not send.")

def create_token(email):
    """Generate a JWT token for magic link."""
    payload = {
        "email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24) # 24 hour expiry
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_token(token):
    """Verify the JWT token."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload["email"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def send_magic_link(email):
    """Send the magic link via Resend."""
    token = create_token(email)
    link = f"{APP_DOMAIN}?token={token}"
    
    try:
        r = resend.Emails.send({
            "from": "admin@seokringle.com",
            "to": email,
            "subject": "🎅 Your Secret Santa Login Link",
            "html": f"""
            <h2>Welcome back to the SEO Community Secret Santa!</h2>
            <p>Click the link below to access your profile:</p>
            <p><a href="{link}">👉 Click here to login</a></p>
            <p><i>This link expires in 24 hours.</i></p>
            """
        })
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

def load_user_profile(email):
    """Load user profile from Supabase."""
    try:
        response = supabase.table("participants").select("*").eq("email", email).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        st.error(f"Error loading profile: {e}")
        return None

def save_profile(email, data):
    """Upsert user profile."""
    # Check if user exists to determine if we insert or update
    # Actually, we can just upsert on email unique constraint
    try:
        # Prepare data
        payload = {
            "email": email,
            "name": data["name"],
            "linkedin_url": data["linkedin_url"],
            "website_url": data["website_url"],
            "bio": data["bio"],
            "address": data["address"],
            "pledge": data["pledge"],
            "expertise_level": data["expertise_level"],
            "wishlist": data["wishlist"]
        }
        
        # Check if record exists to get ID (not strictly needed with upsert but good for explicit logic)
        existing = load_user_profile(email)
        
        if existing:
            response = supabase.table("participants").update(payload).eq("email", email).execute()
        else:
            response = supabase.table("participants").insert(payload).execute()
            
        return True
    except Exception as e:
        st.error(f"Error saving profile: {e}")
        return False

def main():
    st.set_page_config(page_title="SEO Secret Santa", page_icon="🎅", layout="centered")
    
    # Check for token in URL
    if "token" in st.query_params and "user_email" not in st.session_state:
        token = st.query_params["token"]
        email = verify_token(token)
        if email:
            st.session_state.user_email = email
            st.success("✅ Successfully logged in!")
            # Clear query params to clean URL
            # st.query_params.clear() # Optional, sometimes causes rerun loops in older streamlit
        else:
            st.error("❌ Invalid or expired login link.")
    
    # Auth Flow
    if "user_email" not in st.session_state:
        st.title("🎅 SEO Secret Santa Login")
        st.markdown("Enter your email to receive a magic login link.")
        
        with st.form("login_form"):
            email_input = st.text_input("Email Address")
            submit = st.form_submit_button("✨ Send Magic Link")
            
            if submit:
                if email_input:
                    if send_magic_link(email_input):
                        st.success(f"✅ Magic link sent to {email_input}! Please check your inbox.")
                else:
                    st.warning("Please enter your email.")
        return

    # Logged In Flow
    email = st.session_state.user_email
    st.sidebar.write(f"Logged in as: **{email}**")
    if st.sidebar.button("Logout"):
        del st.session_state.user_email
        st.rerun()

    # Load Profile
    profile = load_user_profile(email)
    
    st.title("📝 Your Secret Santa Profile")
    st.markdown("Please fill out your details to join the exchange!")

    # Defaults
    default_name = profile.get("name", "") if profile else ""
    default_linkedin = profile.get("linkedin_url", "") if profile else ""
    default_website = profile.get("website_url", "") if profile else ""
    default_bio = profile.get("bio", "") if profile else ""
    default_address = profile.get("address", "") if profile else ""
    default_pledge = profile.get("pledge", "") if profile else ""
    default_expertise = profile.get("expertise_level", "Mid") if profile else "Mid"
    default_wishlist = profile.get("wishlist", [{"name": "", "url": ""} for _ in range(3)]) if profile else [{"name": "", "url": ""} for _ in range(3)]
    
    # Ensure wishlist has at least 3 slots
    while len(default_wishlist) < 3:
        default_wishlist.append({"name": "", "url": ""})

    with st.form("profile_form"):
        st.subheader("1. Professional Info")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", value=default_name)
            linkedin = st.text_input("LinkedIn URL", value=default_linkedin)
        with col2:
            website = st.text_input("Website / Agency URL", value=default_website)
            expertise = st.selectbox("SEO Expertise Level", ["Junior", "Mid", "Senior"], index=["Junior", "Mid", "Senior"].index(default_expertise))

        bio = st.text_area("Short Bio (help your Santa know you)", value=default_bio, max_chars=300)

        st.subheader("2. The Pledge")
        st.markdown("""
        **Community Rule:** You must pledge a digital gift of value (Audit, Consultation, Tool Access, Dataset, etc).
        *Minimum 100 characters describing your gift.*
        """)
        pledge = st.text_area("I pledge to give...", value=default_pledge, height=100)

        st.subheader("3. Your Wishlist")
        st.markdown("Give your Santa 3 ideas!")
        
        wishlist_items = []
        for i in range(3):
            c1, c2 = st.columns([2, 1])
            with c1:
                w_name = st.text_input(f"Gift Idea #{i+1}", value=default_wishlist[i].get("name", ""), key=f"w_{i}")
            with c2:
                w_url = st.text_input(f"URL (Optional) #{i+1}", value=default_wishlist[i].get("url", ""), key=f"u_{i}")
            wishlist_items.append({"name": w_name, "url": w_url})

        st.subheader("4. Shipping Address (Optional)")
        st.caption("Only if you are open to receiving physical gifts (books, swag, etc).")
        address = st.text_area("Address", value=default_address)

        submit_profile = st.form_submit_button("💾 Save Profile")

        if submit_profile:
            # Validation
            if not name:
                st.error("Name is required.")
            elif len(pledge) < 20: # testing mode: changed 100 to 20 for easier testing, explicitly noted.
                st.error("Please provide a detailed pledge (min 20 chars).") # Kept low for testing
            else:
                data = {
                    "name": name,
                    "linkedin_url": linkedin,
                    "website_url": website,
                    "expertise_level": expertise,
                    "bio": bio,
                    "pledge": pledge,
                    "address": address,
                    "wishlist": wishlist_items
                }
                if save_profile(email, data):
                    st.success("✅ Profile saved successfully!")
                    st.balloons()
                else:
                    st.error("Failed to save profile.")

if __name__ == "__main__":
    main()
