# 🎄 Secret Santa Gift Exchange

A beautiful, mobile-friendly web app for organizing Secret Santa gift exchanges with wishlists, PIN security, and an exciting reveal animation!

![Secret Santa](https://img.shields.io/badge/Secret%20Santa-Gift%20Exchange-red?style=for-the-badge&logo=gift)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)

## ✨ Features

### 🎁 For Users
- **Name Selection** - Choose your name from a dropdown (no typing errors!)
- **PIN Security** - Each person gets a unique 4-digit PIN to access their match
- **Exciting Reveal** - Spinning animation builds anticipation before revealing your match
- **Wishlist System** - Add up to 3 gift ideas with optional product URLs
- **Mobile Friendly** - Fully responsive design works perfectly on phones and tablets
- **Wishlist Updates** - Edit your wishlist anytime

### 👨‍👩‍👧‍👦 Smart Matching
- **Kids Exchange** - Children (7 participants) exchange among themselves
- **Adults Exchange** - Parents (11 participants) exchange among themselves
- **No Self-Matching** - Algorithm ensures no one gets themselves

### 🔒 Security & Privacy
- **PIN Protection** - 4-digit PIN required to see your Secret Santa match
- **Secure Data** - Data file excluded from repository
- **No Snooping** - Can't see others' matches without their PIN

### ⚙️ Admin Features
- **Password Protected** - Admin panel secured with password
- **Generate Assignments** - One-click Secret Santa matching
- **Generate PINs** - Automatic unique PIN generation for all participants
- **PIN Distribution** - View all PINs to share privately
- **Statistics Dashboard** - Track wishlists, assignments, and PINs
- **Clear Functions** - Clear wishlists or all data as needed

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/riadjoseph/secret-santa.git
cd secret-santa
```

2. **Create a virtual environment (recommended)**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the app**
```bash
streamlit run secret_santa_streamlit.py
```

5. **Open your browser**
- The app will automatically open at `http://localhost:8501`
- Or visit the URL shown in the terminal

## 📱 User Guide

### For Participants

#### 1. Enter Your Wishlist
1. Go to **📝 Enter Your Wishlist** tab
2. Select your name from the dropdown
3. Add up to 3 gift ideas (URLs are optional)
4. Click **💾 Save My Wishlist**
5. You can update your wishlist anytime!

#### 2. Find Your Match
1. Go to **🎁 Find Your Match** tab
2. Select your name from the dropdown
3. Enter your 4-digit PIN (received from the admin)
4. Click **🎁 Reveal My Secret Santa Match**
5. Watch the exciting animation! 🎉
6. See who you're buying for and their wishlist

### For Admins

#### Initial Setup
1. Open the sidebar (click the arrow in the top-left)
2. Enter admin password: `x` (change this!)
3. Click **🔄 Generate New Assignments**
4. Click **🔑 Generate PINs for All**
5. Share PINs privately with each participant

#### Admin Panel Features
- **📊 Statistics** - View participant counts and completion status
- **🔑 PINs for Distribution** - Copy/paste PINs to share
- **🗑️ Clear All Wishlists** - Reset all wishlists (keeps assignments)
- **🗑️ Clear All Data** - Start fresh (requires confirmation)

## 👥 Pre-loaded Participants

The app comes pre-configured with 18 participants:

**👶 Kids (7):**
- kid 1
- kid 2
- ...

**👨 Adults (11):**
- adult 1
- adult 2
- ...
- 

## 🎨 User Experience

### Mobile Optimized
- Touch-friendly buttons (44px minimum)
- Responsive text sizing
- Optimized padding and spacing
- No zoom on input focus (iOS)
- Sidebar collapses by default on mobile

### Exciting Animations
- **Spinning Gift** 🎁 - Rotating animation while matching
- **Pulsing Text** - "Finding your Secret Santa match..."
- **Blinking Sparkles** ✨ - Sequential sparkle animation
- **Balloons** 🎈 - Celebration when match is revealed
- **2-second buildup** - Perfect anticipation time

### Intuitive Interface
- **Tab Navigation** - Easy switching between features
- **Dropdown Selectors** - No typing errors with names
- **Status Indicators** - See who completed their wishlist
- **Help Text** - Tooltips and instructions throughout
- **Error Messages** - Clear feedback on what to do

## 🛠️ Technical Details

### Tech Stack
- **Frontend**: Streamlit
- **Backend**: Python 3.8+
- **Data Storage**: JSON file (local)
- **Styling**: Custom CSS with animations

### Data Structure
```json
{
  "participants": {
    "Name": {
      "is_kid": true/false,
      "wishlist": [
        {"name": "Gift idea", "url": "https://..."}
      ],
      "pin": "1234"
    }
  },
  "assignments": {
    "Giver": "Receiver"
  }
}
```

### Security Notes
- `secret_santa_data.json` is excluded from Git (contains PINs and assignments)
- Admin password should be changed in production
- PINs are randomly generated (1000-9999)
- Each PIN is unique

## 🎯 Workflow

1. **Admin**: Generate assignments
2. **Admin**: Generate PINs
3. **Admin**: Share PINs privately with each person
4. **Everyone**: Add their wishlist
5. **Everyone**: Use their PIN to find their match
6. **Everyone**: Shop for their Secret Santa match!

## 📝 Customization

### Change Admin Password
Edit line 190 in `secret_santa_streamlit.py`:
```python
if admin_password == "YOUR_NEW_PASSWORD":
```

### Modify Participants
Edit the `load_data()` function to add/remove participants or change the kids/adults split.

### Adjust Reveal Animation
Modify the `time.sleep(2)` value in line 346 to change animation duration.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

This project is open source and available for personal and commercial use.

## 🎁 Credits

Built with ❤️ using Streamlit

---

**Enjoy your Secret Santa gift exchange! 🎄🎁**
