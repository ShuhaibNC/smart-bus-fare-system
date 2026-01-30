import serial
import time

PORT = "COM12"
BAUD = 115200


def write_nfc(uid, name, delete=False):
    """
    Controls ESP32 RFID logic from Django
    """

    ser = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(2)

    ser.write(b"START\n")

    start = time.time()
    old_data = None

    while time.time() - start < 20:
        if ser.in_waiting:
            msg = ser.readline().decode().strip()
            print("ESP32:", msg)

            if msg == "PLACE_CARD":
                return {"status": "waiting"}

            if msg.startswith("CARD_HAS_DATA"):
                _, old_id, old_name = msg.split(",", 2)
                old_data = {"id": old_id, "name": old_name}
                return {"status": "exists", "data": old_data}

            if msg == "CARD_EMPTY":
                break

    if delete:
        ser.write(b"DELETE\n")
        time.sleep(1)

    ser.write(f"WRITE,{uid},{name}\n".encode())

    start = time.time()
    while time.time() - start < 15:
        if ser.in_waiting:
            msg = ser.readline().decode().strip()
            if msg == "WRITE_SUCCESS":
                ser.close()
                return {"status": "success"}

    ser.close()
    return {"status": "failed"}
