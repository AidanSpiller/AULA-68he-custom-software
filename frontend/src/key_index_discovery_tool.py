"""
This tool will be used to remap keys one by one as a way to scribe the indices values in a faster way than tracking the packages manually
"""

from command_generator import build_key_remap_command
from send_to_keyboard import send_to_keyboard

# Map physical keys to indices
key_index_map = {}
for idx in range(1, 100):  # Try all possible indices
    # Remap key at index 'idx' to 'A' (0x04)
    packet = build_key_remap_command(idx, 0x04)
    send_to_keyboard(packet)
    # Wait for user to press a key and identify which one is now 'A'