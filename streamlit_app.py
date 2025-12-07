import streamlit as st
import time
import os
import jwt
import datetime
import resend
from dotenv import load_dotenv

# Utilities
from utils.db import save_profile, load_user_profile, get_all_participants, save_assignments
from utils.matching import SecretSantaMatcher

# Load environment variables
load_dotenv()

# Helper to get config from secrets (Cloud) or env (Local)
def get_config(key, default=None):
    # Try secrets if available
    try:
        if hasattr(st, "secrets") and key in st.secrets:
            return st.secrets[key]
    except FileNotFoundError:
        pass # No secrets file, fall back to env
    except Exception:
        pass
        
    return os.getenv(key, default)

# Configuration
SUPABASE_URL = get_config("SUPABASE_URL")
SUPABASE_KEY = get_config("SUPABASE_SERVICE_ROLE_KEY") 
RESEND_API_KEY = get_config("RESEND_API_KEY")
APP_DOMAIN = get_config("APP_DOMAIN", "http://localhost:8501")
JWT_SECRET = get_config("SUPABASE_SERVICE_ROLE_KEY") 
JWT_ALGORITHM = "HS256"
ADMIN_EMAILS = [e.strip() for e in get_config("ADMIN_EMAILS", "").split(",") if e.strip()]

# Initialize Resend
if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY
else:
    st.warning("Resend API Key missing. Emails will not send.")

def create_token(email):
    """Generate a JWT token for magic link."""
    payload = {
        "email": email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24) 
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
            "from": "Santa <admin@seokringle.com>",
            "to": email,
            "subject": "🎅 Login to SEO Secret Santa",
            "html": f"""
            <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto;">
                <h2>Welcome back!</h2>
                <p>You requested a secure login link for the SEO Community Secret Santa.</p>
                <div style="margin: 24px 0;">
                    <a href="{link}" style="background-color: #d32f2f; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold;">👉 Click here to Login</a>
                </div>
                <p style="color: #666; font-size: 14px;">If you didn't request this, you can safely ignore this email.</p>
                <p style="color: #666; font-size: 14px;"><i>Link expires in 24 hours.</i></p>
            </div>
            """
        })
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

def render_admin_panel():
    st.header("🔒 Admin Panel")
    st.warning("You are in Admin Mode.")
    
    # Stats
    participants = get_all_participants()
    st.metric("Total Participants", len(participants))
    
    # Actions
    st.subheader("⚙️ Actions")
    if st.button("🎲 Generate Assignments (Run Matching Algorithm)"):
        with st.spinner("Running sophisticated matching logic..."):
            matcher = SecretSantaMatcher(participants)
            assignments = matcher.run_match()
            
            if assignments:
                # Save to DB
                if save_assignments(assignments):
                    st.success(f"✅ Created {len(assignments)} assignments successfully!")
                    st.json(assignments) # Debug view
                else:
                    st.error("❌ Failed to save assignments to DB.")
            else:
                st.error("❌ Algorithm failed to find a valid matching.")

def main():
    st.set_page_config(page_title="SEO Secret Santa", page_icon="🎅", layout="centered")
    
    # Check for token in URL
    if "token" in st.query_params and "user_email" not in st.session_state:
        token = st.query_params["token"]
        email = verify_token(token)
        if email:
            st.session_state.user_email = email
            st.success("✅ Successfully logged in!")
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
    
    # Admin Check
    is_admin = email in ADMIN_EMAILS
    if is_admin:
        st.sidebar.success("🔑 Admin Access")
        mode = st.sidebar.radio("Mode", ["My Profile", "Admin Panel"])
    else:
        mode = "My Profile"

    if st.sidebar.button("Logout"):
        del st.session_state.user_email
        st.rerun()

    if mode == "Admin Panel":
        render_admin_panel()
    else:
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
                if not name:
                    st.error("Name is required.")
                elif len(pledge) < 20: 
                    st.error("Please provide a detailed pledge.")
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
