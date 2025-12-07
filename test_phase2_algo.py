import sys
import pandas as pd
from utils.matching import SecretSantaMatcher, verify_derangement

# Mock data
mock_participants = [
    # Seniors
    {"email": "sr1@test.com", "name": "Senior 1", "expertise_level": "Senior"},
    {"email": "sr2@test.com", "name": "Senior 2", "expertise_level": "Senior"},
    
    # Juniors
    {"email": "jr1@test.com", "name": "Junior 1", "expertise_level": "Junior"},
    {"email": "jr2@test.com", "name": "Junior 2", "expertise_level": "Junior"},
    {"email": "jr3@test.com", "name": "Junior 3", "expertise_level": "Junior"},
    
    # Mids
    {"email": "mid1@test.com", "name": "Mid 1", "expertise_level": "Mid"},
    {"email": "mid2@test.com", "name": "Mid 2", "expertise_level": "Mid"},
]

def test_matching():
    print("--- Testing Matching Algorithm ---")
    matcher = SecretSantaMatcher(mock_participants)
    assignments = matcher.run_match()
    
    print(f"Total Participants: {len(mock_participants)}")
    print(f"Total Assignments: {len(assignments)}")
    
    # Verify everyone is assigned
    if len(assignments) != len(mock_participants):
        print(f"❌ Error: Not everyone was assigned. got {len(assignments)}")
        return
    
    # Verify Derangement (No self-match)
    if verify_derangement(assignments):
        print("✅ Derangement Check Passed (No self-matches)")
    else:
        print("❌ Derangement Check FAILED")
        for g, r in assignments.items():
            if g == r:
                print(f"   Self-match found: {g}")

    # Verify Logic: Seniors -> Juniors
    # We expect SR1 and SR2 to be assigned to Juniors
    print("\nVerifying Senior Assignments:")
    seniors = ["sr1@test.com", "sr2@test.com"]
    juniors = ["jr1@test.com", "jr2@test.com", "jr3@test.com"]
    
    senior_matches_valid = 0
    for sr in seniors:
        receiver = assignments.get(sr)
        print(f"  {sr} -> {receiver}")
        if receiver in juniors:
            senior_matches_valid += 1
            
    if senior_matches_valid == len(seniors):
        print("✅ All Seniors matched with Juniors priority")
    else:
        print(f"⚠️  Only {senior_matches_valid}/{len(seniors)} Seniors matched with Juniors")

    print("\nFull Assignments Map:")
    for k, v in assignments.items():
        print(f"{k} -> {v}")

if __name__ == "__main__":
    test_matching()
