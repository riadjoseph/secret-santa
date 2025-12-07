Readme · MD
Copy

🎄 Secret Santa Streamlit App
A web-based Secret Santa gift exchange application where participants can register and privately discover who they're buying for.

Features
✅ Participant Registration

Enter your name and family name
Indicate if you're a kid (son/daughter under 18) or adult
Each participant registers individually
✅ Privacy-Focused

Participants only see their own match
No one can see the complete list of assignments
Keep the secret safe!
✅ Family Constraints

Kids exchange gifts among themselves
Adults exchange gifts among themselves
No one gets someone from their own family
✅ Admin Panel

Generate assignments when everyone is registered
View statistics (number of kids, adults, families)
Clear all data if needed
How to Run
Option 1: Local Installation
Install Python 3.8 or higher
Install dependencies:
bash
pip install -r requirements.txt
Run the app:
bash
streamlit run secret_santa_streamlit.py
Open your browser to the URL shown (usually http://localhost:8501)
Option 2: Quick Start (without installation)
bash
# Install streamlit if you don't have it
pip install streamlit

# Run the app
streamlit run secret_santa_streamlit.py
How to Use
Step 1: Registration Phase
Share the app URL with all participants
Each person goes to the "Register" tab
Fill in:
Full name (exactly as they want it to appear)
Family name (everyone in the same household uses the same family name)
Are you a kid? Yes/No
Click "Register"
Step 2: Generate Assignments (Admin Only)
Once ALL participants are registered
Go to the Admin Panel in the sidebar
Click "🔄 Generate New Assignments"
The app will create valid assignments automatically
Step 3: Participants Find Their Match
Each person goes to "Find Your Match" tab
Enters their name exactly as registered
Clicks "Reveal My Secret Santa Match"
They'll see who they're buying for (ONLY their match, not the full list!)
Data Storage
All data is stored in secret_santa_data.json
This file is created automatically when the app runs
To reset everything, use the "Clear All Data" button in admin panel
Keep this file secure to maintain the secret!
Example Usage
Registration:

Ana (Family: Garcia, Kid: No)
Pau (Family: Garcia, Kid: Yes)
Victor (Family: Smith, Kid: Yes)
Britta (Family: Smith, Kid: No)
After generating assignments:

Kids exchange: Pau ↔ Victor
Adults exchange: Ana ↔ Britta
Each person only sees their own match when they look it up!

Troubleshooting
"Not enough participants" error:

You need at least 2 kids AND 2 adults
Make sure all participants have registered
"Name not found" error:

Check spelling - names must match exactly
Names are case-sensitive
Want to regenerate assignments:

Just click "Generate New Assignments" again
This will create a completely new random assignment
Security Note
⚠️ This app stores data in a local JSON file. If you need this on a server accessible to multiple people:

Consider adding password protection
Use a proper database
Deploy on a secure platform (like Streamlit Cloud with authentication)
For family use on a local network, the current setup is fine!

Support
If you encounter any issues:

Make sure all participants are registered
Check the Admin Panel statistics
Try clearing data and starting fresh if needed
