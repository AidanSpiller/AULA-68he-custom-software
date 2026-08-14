from src.send_to_keyboard import send_to_keyboard
from src.command_generator import build_key_remap_command

def manual_remap_test():
    print("--- Starting Aula Hero 68HE Hardware Test ---")
    
    # 0x46 is the matrix index for spacebar, 0x2C is USB code for space 
    key_index = 0x46
    keycode = 0x2C 
    
    packet = build_key_remap_command(key_index, keycode)
    
    print("Generated Packet Bytes:")
    print(packet.hex(' '))
    
    print("\nAttempting connection to device...")
    success = send_to_keyboard(packet)
    
    if success:
        print("\nSUCCESS: Packet safely transmitted to keyboard report!")
    else:
        print("\nFAILURE: Check USB connection or HID configuration.")

if __name__ == "__main__":
    manual_remap_test()
