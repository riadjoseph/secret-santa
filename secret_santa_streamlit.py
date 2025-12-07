import streamlit as st
import json
import random
from pathlib import Path
from typing import Dict, List, Set
import hashlib
import time

# File to store participant data and assignments
DATA_FILE = "secret_santa_data.json"

def load_data():
    """Load participant data and assignments from file."""
    if Path(DATA_FILE).exists():
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {
        "participants": {
            # Kids
            "Aria": {"is_kid": True, "wishlist": [], "pin": None},
            "Lúa": {"is_kid": True, "wishlist": [], "pin": None},
            "Mattes": {"is_kid": True, "wishlist": [], "pin": None},
            "Pau": {"is_kid": True, "wishlist": [], "pin": None},
            "Sasha": {"is_kid": True, "wishlist": [], "pin": None},
            "Scarlett": {"is_kid": True, "wishlist": [], "pin": None},
            "Victor": {"is_kid": True, "wishlist": [], "pin": None},
            # Parents
            "Alok": {"is_kid": False, "wishlist": [], "pin": None},
            "Ana": {"is_kid": False, "wishlist": [], "pin": None},
            "Bora": {"is_kid": False, "wishlist": [], "pin": None},
            "Britta": {"is_kid": False, "wishlist": [], "pin": None},
            "Caro": {"is_kid": False, "wishlist": [], "pin": None},
            "Güimi": {"is_kid": False, "wishlist": [], "pin": None},
            "Jelena": {"is_kid": False, "wishlist": [], "pin": None},
            "Laurent": {"is_kid": False, "wishlist": [], "pin": None},
            "Priyanka": {"is_kid": False, "wishlist": [], "pin": None},
            "Puja": {"is_kid": False, "wishlist": [], "pin": None},
            "Riad": {"is_kid": False, "wishlist": [], "pin": None}
        },
        "assignments": {}
    }

def save_data(data):
    """Save participant data and assignments to file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def generate_pins(data):
    """Generate random 4-digit PINs for all participants."""
    used_pins = set()
    for name in data["participants"]:
        # Generate unique 4-digit PIN
        while True:
            pin = str(random.randint(1000, 9999))
            if pin not in used_pins:
                used_pins.add(pin)
                data["participants"][name]["pin"] = pin
                break
    return data

def create_secret_santa_assignments(data):
    """
    Create Secret Santa assignments ensuring:
    - Kids exchange among themselves
    - Adults exchange among themselves
    """
    participants = data["participants"]

    # Separate kids and adults
    kids = [name for name, info in participants.items() if info["is_kid"]]
    adults = [name for name, info in participants.items() if not info["is_kid"]]

    def find_valid_assignment(people, max_attempts=1000):
        """Find a valid Secret Santa assignment."""
        for attempt in range(max_attempts):
            givers = people.copy()
            receivers = people.copy()
            random.shuffle(receivers)

            assignment = {}

            for giver, receiver in zip(givers, receivers):
                # Ensure no one gets themselves
                if giver == receiver:
                    break
                assignment[giver] = receiver
            else:
                # All assignments are valid
                return assignment

        raise ValueError(f"Could not find valid assignment after {max_attempts} attempts")

    # Create assignments for both groups
    assignments = {}

    if len(kids) > 0:
        if len(kids) < 2:
            raise ValueError("Need at least 2 kids to create assignments")
        kids_assignments = find_valid_assignment(kids)
        assignments.update(kids_assignments)

    if len(adults) > 0:
        if len(adults) < 2:
            raise ValueError("Need at least 2 adults to create assignments")
        adults_assignments = find_valid_assignment(adults)
        assignments.update(adults_assignments)

    return assignments

def main():
    st.set_page_config(
        page_title="🎄 Secret Santa",
        page_icon="🎁",
        layout="centered",
        initial_sidebar_state="collapsed"  # Start with sidebar collapsed on mobile
    )
    
    # Custom CSS - Mobile Friendly
    st.markdown("""
        <style>
        /* Base styles */
        .big-font {
            font-size: 24px !important;
            font-weight: bold;
            color: #2E7D32;
        }
        .receiver-box {
            padding: 20px;
            border-radius: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            font-size: 28px;
            font-weight: bold;
            margin: 20px 0;
        }
        .warning-box {
            padding: 15px;
            border-radius: 5px;
            background-color: #FFF3CD;
            border: 1px solid #FFE69C;
            color: #856404;
            margin: 10px 0;
        }

        /* Mobile responsiveness */
        @media only screen and (max-width: 768px) {
            .receiver-box {
                font-size: 20px;
                padding: 15px;
                margin: 15px 0;
            }

            /* Make form inputs more touch-friendly */
            .stTextInput input {
                font-size: 16px !important;
                min-height: 44px;
            }

            /* Better button sizing for mobile */
            .stButton button {
                width: 100%;
                min-height: 44px;
                font-size: 16px !important;
            }

            /* Adjust title size for mobile */
            h1 {
                font-size: 1.8rem !important;
            }

            h2 {
                font-size: 1.4rem !important;
            }

            h3 {
                font-size: 1.2rem !important;
            }
        }

        /* Prevent zoom on input focus for iOS */
        @media only screen and (max-width: 768px) {
            input, select, textarea {
                font-size: 16px !important;
            }
        }

        /* Make the app container more mobile-friendly */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 100%;
        }

        @media only screen and (max-width: 768px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🎄 Secret Santa Gift Exchange 🎁")
    
    # Load data
    data = load_data()
    
    # Sidebar for admin functions
    with st.sidebar:
        st.header("⚙️ Admin Panel")

        admin_password = st.text_input("Admin Password", type="password", key="admin_pw")

        if admin_password == "santa2024":  # Change this password!
            st.success("✅ Admin access granted")

            if st.button("🔄 Generate New Assignments"):
                if len(data["participants"]) < 2:
                    st.error("Need at least 2 participants to generate assignments!")
                else:
                    try:
                        assignments = create_secret_santa_assignments(data)
                        data["assignments"] = assignments
                        save_data(data)
                        st.success(f"✅ Assignments generated for {len(assignments)} participants!")
                        st.rerun()
                    except ValueError as e:
                        st.error(f"❌ Error: {str(e)}")

            if st.button("🔑 Generate PINs for All"):
                data = generate_pins(data)
                save_data(data)
                st.success("✅ PINs generated for all participants!")
                st.rerun()

            if st.button("🗑️ Clear All Wishlists"):
                # Clear all wishlists but keep participants and assignments
                for participant in data["participants"]:
                    data["participants"][participant]["wishlist"] = []
                save_data(data)
                st.success("All wishlists cleared!")
                st.rerun()

            if st.button("🗑️ Clear All Data"):
                if st.button("⚠️ Confirm Delete"):
                    data = {"participants": {}, "assignments": {}}
                    save_data(data)
                    st.success("All data cleared!")
                    st.rerun()

            st.divider()

            # Show statistics
            st.subheader("📊 Statistics")
            kids_count = sum(1 for p in data["participants"].values() if p["is_kid"])
            adults_count = len(data["participants"]) - kids_count
            wishlists_complete = sum(1 for p in data["participants"].values() if len(p.get("wishlist", [])) > 0)
            pins_generated = sum(1 for p in data["participants"].values() if p.get("pin") is not None)
            st.write(f"👶 Kids: {kids_count}")
            st.write(f"👨 Adults: {adults_count}")
            st.write(f"👥 Total: {len(data['participants'])}")
            st.write(f"🎁 Wishlists: {wishlists_complete}/{len(data['participants'])}")
            st.write(f"🎯 Assignments: {len(data['assignments'])}")
            st.write(f"🔑 PINs: {pins_generated}/{len(data['participants'])}")

            # Display all PINs for distribution
            if pins_generated > 0:
                st.divider()
                st.subheader("🔑 PINs for Distribution")
                st.caption("Share these PINs privately with each participant")

                # Separate kids and adults
                kids = [(name, info) for name, info in data["participants"].items() if info["is_kid"]]
                adults = [(name, info) for name, info in data["participants"].items() if not info["is_kid"]]

                if kids:
                    st.markdown("**👶 Kids:**")
                    for name, info in sorted(kids):
                        pin = info.get("pin", "Not set")
                        st.code(f"{name}: {pin}")

                if adults:
                    st.markdown("**👨 Adults:**")
                    for name, info in sorted(adults):
                        pin = info.get("pin", "Not set")
                        st.code(f"{name}: {pin}")
        elif admin_password:
            st.error("❌ Incorrect password")
    
    # Main content
    tab1, tab2 = st.tabs(["🎁 Find Your Match", "📝 Enter Your Wishlist"])

    with tab1:
        st.header("Find Out Who You're Buying For")

        if not data["assignments"]:
            st.warning("⚠️ No assignments have been generated yet. Please wait for the admin to generate assignments.")
        else:
            # Get sorted list of all participants
            all_participants = sorted(data["participants"].keys())

            col1, col2 = st.columns([2, 1])
            with col1:
                name = st.selectbox(
                    "Select your name:",
                    options=[""] + all_participants,
                    key="lookup_name"
                )
            with col2:
                user_pin = st.text_input(
                    "Your 4-digit PIN:",
                    type="password",
                    max_chars=4,
                    key="user_pin",
                    help="Enter the PIN you received from the admin"
                )

            if st.button("🎁 Reveal My Secret Santa Match", type="primary"):
                if not name:
                    st.error("Please select your name!")
                elif not user_pin:
                    st.error("Please enter your 4-digit PIN!")
                elif name not in data["assignments"]:
                    st.error("❌ Assignments haven't been generated yet. Please wait for the admin.")
                else:
                    # Verify PIN
                    correct_pin = data["participants"][name].get("pin")
                    if correct_pin is None:
                        st.error("❌ PINs haven't been generated yet. Please contact the admin.")
                    elif user_pin != correct_pin:
                        st.error("❌ Incorrect PIN! Please check your PIN and try again.")
                    else:
                        receiver = data["assignments"][name]
                        receiver_info = data["participants"][receiver]
                        wishlist = receiver_info.get("wishlist", [])

                        # Create excitement with spinning animation
                        spinner_placeholder = st.empty()

                        with spinner_placeholder:
                            st.markdown("""
                                <div style="text-align: center; padding: 60px 20px;">
                                    <div style="font-size: 80px; animation: spin 0.8s linear infinite; display: inline-block;">🎁</div>
                                    <h2 style="color: #2E7D32; margin-top: 30px; animation: pulse 1s ease-in-out infinite;">
                                        Finding your Secret Santa match...
                                    </h2>
                                    <div style="margin-top: 20px; font-size: 30px;">
                                        <span style="animation: blink 0.5s ease-in-out infinite;">✨</span>
                                        <span style="animation: blink 0.5s ease-in-out 0.2s infinite;">✨</span>
                                        <span style="animation: blink 0.5s ease-in-out 0.4s infinite;">✨</span>
                                    </div>
                                </div>
                                <style>
                                @keyframes spin {
                                    0% { transform: rotate(0deg); }
                                    100% { transform: rotate(360deg); }
                                }
                                @keyframes pulse {
                                    0%, 100% { opacity: 1; transform: scale(1); }
                                    50% { opacity: 0.7; transform: scale(1.05); }
                                }
                                @keyframes blink {
                                    0%, 100% { opacity: 0.3; }
                                    50% { opacity: 1; }
                                }
                                </style>
                            """, unsafe_allow_html=True)

                        # Wait for 2 seconds to build excitement
                        time.sleep(2)

                        # Clear spinner and show result
                        spinner_placeholder.empty()

                        st.balloons()
                        st.markdown(f'<div class="receiver-box">🎁 You are buying for:<br><br>{receiver}</div>',
                                   unsafe_allow_html=True)

                        if wishlist and len(wishlist) > 0:
                            st.subheader(f"🎁 {receiver}'s Wishlist:")
                            for i, item in enumerate(wishlist, 1):
                                item_name = item.get("name", "")
                                item_url = item.get("url", "")
                                if item_url:
                                    st.markdown(f"{i}. [{item_name}]({item_url})")
                                else:
                                    st.write(f"{i}. {item_name}")
                        else:
                            st.warning(f"⚠️ {receiver} hasn't entered their wishlist yet. Check back later!")

                        st.success("Remember: Keep it a secret! 🤫")

                        # Check if current user has filled their wishlist
                        user_wishlist = data["participants"][name].get("wishlist", [])
                        st.divider()
                        if not user_wishlist or len(user_wishlist) == 0:
                            st.info("💡 **Don't forget:** Add your own wishlist so your Secret Santa knows what to get you!")
                            st.markdown("👉 **Click on the '📝 Enter Your Wishlist' tab above to add your wishes!**")
                        else:
                            st.success(f"✅ You've already added {len(user_wishlist)} item(s) to your wishlist! You can update it anytime in the '📝 Enter Your Wishlist' tab.")
    
    with tab2:
        st.header("Enter Your Wishlist")
        st.write("Select your name and add up to 3 gift ideas (URLs are optional)")

        # Get sorted list of all participants
        all_participants_wishlist = sorted(data["participants"].keys())

        # Name selector outside form to check for existing wishlist
        lookup_name = st.selectbox(
            "Select your name:",
            options=[""] + all_participants_wishlist,
            key="wishlist_name_lookup"
        )

        # Check if user has existing wishlist
        existing_wishlist = []
        if lookup_name and lookup_name in data["participants"]:
            existing_wishlist = data["participants"][lookup_name].get("wishlist", [])
            if existing_wishlist:
                st.info(f"ℹ️ You have an existing wishlist. You can update it below.")

        with st.form("wishlist_form"):
            st.subheader("Your Wishes:")

            # Pre-fill with existing values if available
            wish1_name = st.text_input("Gift Idea 1",
                                       value=existing_wishlist[0]["name"] if len(existing_wishlist) > 0 else "",
                                       placeholder="e.g., LEGO Star Wars Set", key="w1")
            wish1_url = st.text_input("URL for Gift 1 (optional)",
                                      value=existing_wishlist[0]["url"] if len(existing_wishlist) > 0 else "",
                                      placeholder="https://...", key="u1")

            wish2_name = st.text_input("Gift Idea 2",
                                       value=existing_wishlist[1]["name"] if len(existing_wishlist) > 1 else "",
                                       placeholder="e.g., Nike Sneakers", key="w2")
            wish2_url = st.text_input("URL for Gift 2 (optional)",
                                      value=existing_wishlist[1]["url"] if len(existing_wishlist) > 1 else "",
                                      placeholder="https://...", key="u2")

            wish3_name = st.text_input("Gift Idea 3",
                                       value=existing_wishlist[2]["name"] if len(existing_wishlist) > 2 else "",
                                       placeholder="e.g., Wireless Headphones", key="w3")
            wish3_url = st.text_input("URL for Gift 3 (optional)",
                                      value=existing_wishlist[2]["url"] if len(existing_wishlist) > 2 else "",
                                      placeholder="https://...", key="u3")

            submitted = st.form_submit_button("💾 Save My Wishlist", type="primary")

            if submitted:
                if not lookup_name:
                    st.error("❌ Please select your name!")
                else:
                    # Build wishlist with only filled items
                    wishlist = []
                    if wish1_name:
                        wishlist.append({"name": wish1_name, "url": wish1_url})
                    if wish2_name:
                        wishlist.append({"name": wish2_name, "url": wish2_url})
                    if wish3_name:
                        wishlist.append({"name": wish3_name, "url": wish3_url})

                    # Save wishlist (even if empty)
                    data["participants"][lookup_name]["wishlist"] = wishlist

                    save_data(data)
                    if wishlist:
                        st.success(f"✅ Wishlist saved for {lookup_name} ({len(wishlist)} items)!")
                    else:
                        st.success(f"✅ Wishlist cleared for {lookup_name}!")
                    st.balloons()
                    st.rerun()

        # Show who has completed their wishlist
        if data["participants"]:
            st.divider()
            st.subheader("📋 Wishlist Status")

            # Separate kids and adults
            kids = [(name, info) for name, info in data["participants"].items() if info["is_kid"]]
            adults = [(name, info) for name, info in data["participants"].items() if not info["is_kid"]]

            if kids:
                st.markdown("**👶 Kids:**")
                for name, info in sorted(kids):
                    has_wishlist = len(info.get("wishlist", [])) > 0
                    status = "✅" if has_wishlist else "⏳"
                    st.write(f"{status} {name}")

            if adults:
                st.markdown("**👨 Adults:**")
                for name, info in sorted(adults):
                    has_wishlist = len(info.get("wishlist", [])) > 0
                    status = "✅" if has_wishlist else "⏳"
                    st.write(f"{status} {name}")

if __name__ == "__main__":
    main()