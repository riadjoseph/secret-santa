import random
import pandas as pd
from utils.db import get_all_participants

class SecretSantaMatcher:
    def __init__(self, participants=None):
        """
        participants: list of dicts from DB. If None, fetches from DB.
        """
        if participants is None:
            participants = get_all_participants()
        self.participants = participants
        self.df = pd.DataFrame(participants) if participants else pd.DataFrame()
        
    def run_match(self):
        """
        Execute the matching logic.
        Returns: dict {giver_email: receiver_email}
        """
        if self.df.empty:
            return {}
            
        # 1. Separate by Expertise
        # Standardize casing just in case
        if "expertise_level" in self.df.columns:
            juniors = self.df[self.df["expertise_level"].str.lower() == "junior"]
            mids = self.df[self.df["expertise_level"].str.lower() == "mid"]
            seniors = self.df[self.df["expertise_level"].str.lower() == "senior"]
            # Others or missing? Treat as Mid
            others = self.df[~self.df["expertise_level"].str.lower().isin(["junior", "mid", "senior"])]
            mids = pd.concat([mids, others])
        else:
            # Fallback if column missing
            juniors = pd.DataFrame()
            seniors = pd.DataFrame()
            mids = self.df
        
        assignments = {}
        givers_pool = set(self.df["email"])
        receivers_pool = set(self.df["email"])

        # --- LOGIC: Senior -> Junior Priority ---
        # Try to assign every Senior to a Junior first
        
        senior_emails = list(seniors["email"]) if not seniors.empty else []
        junior_emails = list(juniors["email"]) if not juniors.empty else []
        mid_emails = list(mids["email"]) if not mids.empty else []
        
        random.shuffle(senior_emails)
        random.shuffle(junior_emails)
        random.shuffle(mid_emails)

        # 1. Seniors give to Juniors (as much as possible)
        for senior in senior_emails:
            if junior_emails:
                # Give to a junior
                receiver = junior_emails.pop(0)
                assignments[senior] = receiver
                
                givers_pool.remove(senior)
                receivers_pool.remove(receiver)
            else:
                # No juniors left? Senior gives to Mid?
                pass 

        # 2. Remaining matching (Derangement)
        # We need to take the remaining givers and match them to remaining receivers
        # such that no one gives to themselves.
        
        rem_givers = list(givers_pool)
        rem_receivers = list(receivers_pool)
        
        # Simple derangement attempt
        # If we fail (someone matched to self), we retry (shuffle)
        max_retries = 100
        for _ in range(max_retries):
            random.shuffle(rem_receivers)
            valid = True
            temp_assignments = {}
            
            for g, r in zip(rem_givers, rem_receivers):
                if g == r:
                    valid = False
                    break
                temp_assignments[g] = r
            
            if valid:
                assignments.update(temp_assignments)
                return assignments
        
        # If failed after retries (rare unless n is very small), return empty or error
        print("Failed to find valid matching after retries.")
        return {}

def verify_derangement(assignments):
    """Ensure no one is assigned to themselves."""
    for giver, receiver in assignments.items():
        if giver == receiver:
            return False
    return True
