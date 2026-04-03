import can
import time

_bus = None


def get_bus():
    global _bus
    if _bus is None:
        _bus = can.Bus(interface='socketcan', channel='can0', bitrate=125000)
    return _bus


def read_can_2byte(reg_addr, req_addr, timeout=0.05):
    bus = get_bus()
    try:
        bus.send(can.Message(arbitration_id=req_addr, data=[reg_addr, 0], is_extended_id=False))
        deadline = time.time() + timeout
        while time.time() < deadline:
            msg = bus.recv(timeout=deadline - time.time())
            if msg is None:
                break
            if msg.arbitration_id == reg_addr:
                if len(msg.data) == 2:
                    return msg.data[0] + msg.data[1] * 256
        print(f"Timeout beim Lesen (reg=0x{reg_addr:02X}, req=0x{req_addr:02X})")
    except Exception as e:
        global _bus
        _bus = None
        print(f"Fehler beim Lesen (reg=0x{reg_addr:02X}): {e}")
        return 0


def read_can_str(reg_addr, req_addr, timeout=0.05):
    bus = get_bus()
    try:
        bus.send(can.Message(arbitration_id=req_addr, data=[reg_addr, 0], is_extended_id=False))
        deadline = time.time() + timeout
        while time.time() < deadline:
            msg = bus.recv(timeout=deadline - time.time())
            if msg is None:
                break
            if msg.arbitration_id == reg_addr:
                return "".join(chr(b) for b in msg.data)
        print(f"Timeout beim Lesen (reg=0x{reg_addr:02X}, req=0x{req_addr:02X})")
    except Exception as e:
        global _bus
        _bus = None
        print(f"Fehler beim Lesen (reg=0x{reg_addr:02X}): {e}")
        return ""


def write_can(reg_addr, val):
    bus = get_bus()
    msg = can.Message(
        arbitration_id=reg_addr,
        data=[val % 256, (val // 256) % 256],
        is_extended_id=False
    )
    try:
        bus.send(msg)
    except Exception as e:
        global _bus
        _bus = None
        print(f"Fehler beim Schreiben (reg=0x{reg_addr:02X}): {e}")
        return 0


def write_can_str(reg_addr, val):
    bus = get_bus()
    msg = can.Message(
        arbitration_id=reg_addr,
        data=list(val.encode('utf-8')),
        is_extended_id=False
    )
    try:
        bus.send(msg)
    except Exception as e:
        global _bus
        _bus = None
        print(f"Fehler beim Schreiben (reg=0x{reg_addr:02X}): {e}")
        return 0
