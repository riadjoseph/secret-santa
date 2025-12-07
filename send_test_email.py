import os
import resend
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.environ.get("RESEND_API_KEY")

email_domain = os.environ.get("APP_DOMAIN", "https://seokringle.com")
# Extract domain from url if possible or just use a default sender
sender_email = "onboarding@resend.dev" # Default for testing until domain is verified
to_email = "riadjoseph@gmail.com" # Placeholder, will ask user or use env

print(f"Sending test email from {sender_email} to {to_email}...")

try:
    r = resend.Emails.send({
        "from": sender_email,
        "to": to_email,
        "subject": "🎅 Secret Santa Test: Magic Link",
        "html": f"<p>Ho ho ho! 🎄<br>This is a test email from your Secret Santa app.<br><a href='{email_domain}'>Click here to access the app</a></p>"
    })
    print(f"✅ Email sent! ID: {r.get('id')}")
except Exception as e:
    print(f"❌ Failed to send email: {e}")
