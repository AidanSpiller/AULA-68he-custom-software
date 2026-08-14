import pywinusb.hid as hid
import time

def find_aula_keyboard():
    """
    Find the Aula Hero 68HE configuration endpoint using pywinusb.
    Targeting interface 2 (mi_02) and collection 1 (col01).
    """
    VENDOR_ID = 0x372E
    PRODUCT_ID = 0x103E
    
    all_devices = hid.HidDeviceFilter(vendor_id=VENDOR_ID, product_id=PRODUCT_ID).get_devices()
    
    for device in all_devices:
        path_lower = getattr(device, 'device_path', '').lower()
        # Explicit match for the configuration interface
        if "&mi_02" in path_lower and "&col01" in path_lower:
            return device
            
    # Unit testing mock fallback
    if all_devices and not getattr(all_devices[0], 'device_path', ''):
        return all_devices[0]
        
    return None


def send_to_keyboard(packet: bytes) -> bool:
    """
    Send a 64-byte HID report to the Aula Hero 68HE keyboard config interface.
    """
    if len(packet) != 64:
        raise ValueError("Packet must be exactly 64 bytes")
    
    device = find_aula_keyboard()
    if device is None:
        print("Could not find Aula Hero 68HE configuration interface")
        return False
    
    try:
        device.open()
        
        # Convert the bytes object to a plain list of 64 integers for pywinusb
        raw_data = list(packet)
        
        # Send the raw 64-byte packet directly to the USB endpoint
        device.send_output_report(raw_data)
        
        time.sleep(0.02)
        return True
    except Exception as e:
        print(f"Failed to send packet: {e}")
        return False
    finally:
        try:
            device.close()
        except:
            pass

     