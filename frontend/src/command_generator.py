from checksum import calculate_checksum


def build_key_remap_command(key_index: int, keycode: int) -> bytes:
    """
    Build a complete 64-byte HID report for remapping a key.
    
    Args:
        key_index: The key's index in the keyboard matrix
        keycode: The USB HID keycode to assign
    
    Returns:
        64-byte packet ready to send to the keyboard
    """
    # Start with the fixed header and zeros
    packet = bytearray(64)
    packet[0] = 0x09  # Report ID
    packet[1] = 0x03  # Command: Key Remapping
    packet[4] = 0x01  # Flag (always seems to be 1)
    packet[6] = 0x06  # Row/Column info (might vary per key)
    packet[8] = key_index  # Which key to remap
    packet[12] = keycode  # What key to map to
    
    # Calculate and set checksum
    packet[63] = calculate_checksum(bytes(packet[:63]))
    
    return bytes(packet)

def build_actuation_command(key_index: int, actuation_mm: float) -> bytes:
    """
    Build a complete 64-byte HID report for setting actuation point.
    
    Args:
        key_index: The key's index in the keyboard matrix
        actuation_mm: Actuation distance in millimeters (e.g., 1.0, 2.5)
    
    Returns:
        64-byte packet ready to send to the keyboard
    """
    # Encode actuation value (1.0mm = 100 = 0x64)
    actuation_value = round(actuation_mm * 100)
    
    # This is the "set value" packet (0x13 command)
    packet = bytearray(64)
    packet[0] = 0x09
    packet[1] = 0x13  # Command: Set Actuation
    packet[4] = 0x01
    packet[6] = 0x05
    packet[8] = 0x01
    packet[10] = actuation_value & 0xFF
    packet[11] = 0x01
    
    # Calculate and set checksum
    packet[63] = calculate_checksum(bytes(packet[:63]))
    
    return bytes(packet)