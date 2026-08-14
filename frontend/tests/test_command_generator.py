from src.command_generator import build_key_remap_command, build_actuation_command
from src.checksum import verify_packet

"""
   This test will verify that every generated packet
   
   1. Is exactly 64 bytes
   
   2. Target variables, such as key_index, keycode, and actuation_mm are in their proper byte positions
   
   3. final byte must correctly match the calculate_checksum algorithm
"""

def test_build_key_remap_command():
    # Arrange
    key_index = 0x0f # 1 key
    key_code = 0x08 # keycode for E
    
    # Act
    packet = build_key_remap_command(key_index, key_code)
    
    # Assert structural integrity
    assert len(packet) == 64
    assert verify_packet(packet) is True
    
    # Assert jeader values and payload offsets
    assert packet[0] == 0x09 # header
    assert packet[1] == 0x03 # command type
    assert packet[4] == 0x01 # seems to be a set value
    assert packet[6] == 0x06 # appears in all rebind commands
    assert packet[8] == key_index
    assert packet[12] == key_code
    
def test_build_actuation_command():
    # Arrange
    key_idx = 0x05
    actuation_mm = 1.45  # Stored as 145 -> 0x91
    
    # Act
    packet = build_actuation_command(key_idx, actuation_mm)
    
    # Assert structural integrity
    assert len(packet) == 64
    assert verify_packet(packet) is True
    
    # Assert header values and payload offsets
    assert packet[0] == 0x09
    assert packet[1] == 0x13
    assert packet[4] == 0x01
    assert packet[6] == 0x05
    assert packet[8] == 0x01
    assert packet[10] == 145  # 0x91
    assert packet[11] == 0x01

def test_actuation_floating_point_rounding():
    # Tests that floating point issues (e.g. 2.3 * 100 = 229.99999999999997) 
    # don't break the integer cast if handled poorly by the source code.
    packet = build_actuation_command(1, 2.3)

    assert packet[10] == 230  