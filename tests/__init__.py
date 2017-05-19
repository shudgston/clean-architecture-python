"""
Top-level setup for any unit test
"""

from links.security import lower_rounds

print("--- TOP LEVEL TEST SETUP ---")

# lower amount of rounds when hashing passwords, for faster tests
lower_rounds()

