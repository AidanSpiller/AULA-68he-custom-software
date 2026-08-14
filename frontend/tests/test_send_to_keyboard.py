import pytest
from unittest.mock import MagicMock, patch
from src.send_to_keyboard import send_to_keyboard

@patch('src.send_to_keyboard.hid.HidDeviceFilter')
def test_send_to_keyboard_success(mock_filter_class):
    mock_device = MagicMock()
    # Mocking the discovery path matching our mi_02 col01 filter rule
    mock_device.device_path = "vid_372e&pid_103e&mi_02&col01"
    
    mock_report = MagicMock()
    mock_device.find_output_reports.return_value = [mock_report]
    
    mock_filter_instance = mock_filter_class.return_value
    mock_filter_instance.get_devices.return_value = [mock_device]
    
    packet = bytes([0x09] + [0x00] * 62 + [0x7A])
    result = send_to_keyboard(packet)

    assert result is True
    mock_device.open.assert_called_once()
    mock_report.send.assert_called_once()
    mock_device.close.assert_called_once()

def test_send_to_keyboard_invalid_length():
    # Verify length validation protection works
    invalid_packet = bytes([0x01, 0x02, 0x03])
    with pytest.raises(ValueError, match="Packet must be exactly 64 bytes"):
        send_to_keyboard(invalid_packet)
