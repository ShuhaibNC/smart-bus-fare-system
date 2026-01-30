import serial
import time

# ===============================
# CONFIG
# ===============================
SERIAL_PORT = "COM12"     # ✅ confirmed from Device Manager
BAUD_RATE = 115200
TIMEOUT = 5               # seconds


# ===============================
# SERIAL HANDLER
# ===============================
class NFCWriter:
    def __init__(self):
        self.ser = serial.Serial(
            SERIAL_PORT,
            BAUD_RATE,
            timeout=1
        )
        time.sleep(2)  # allow ESP32 reset
        self._wait_for_ready()

    def _wait_for_ready(self):
        """Wait for ESP32 to say READY"""
        start = time.time()
        while time.time() - start < TIMEOUT:
            line = self._read()
            if line == "READY":
                return
        raise RuntimeError("ESP32 not responding")

    def _read(self):
        """Read one line from ESP32"""
        if self.ser.in_waiting:
            return self.ser.readline().decode().strip()
        return None

    def _send(self, msg):
        """Send command to ESP32"""
        self.ser.write((msg + "\n").encode())

    # ===============================
    # PUBLIC FUNCTIONS (USE THESE)
    # ===============================

    def write_card(self, student_id, name):
        """
        WRITE:<ID>:<NAME>
        """
        self._send(f"WRITE:{student_id}:{name}")

        while True:
            resp = self._read()
            if not resp:
                continue

            # ---- ESP32 responses ----
            if resp == "PLACE_CARD":
                return {"status": "place_card"}

            if resp.startswith("EXISTING:"):
                _, cid, cname = resp.split(":", 2)
                return {
                    "status": "existing",
                    "card_id": cid,
                    "name": cname
                }

            if resp == "WRITE_OK":
                return {"status": "success"}

    def delete_card(self):
        """
        DELETE
        """
        self._send("DELETE")

        while True:
            resp = self._read()
            if not resp:
                continue

            if resp == "PLACE_CARD":
                return {"status": "place_card"}

            if resp == "DELETED":
                return {"status": "deleted"}

    def close(self):
        self.ser.close()


# ===============================
# SIMPLE FUNCTION WRAPPERS
# (easy to call from Django)
# ===============================

def write_nfc(student_id, name):
    nfc = NFCWriter()
    result = nfc.write_card(student_id, name)
    nfc.close()
    return result


def delete_nfc():
    nfc = NFCWriter()
    result = nfc.delete_card()
    nfc.close()
    return result

nfc = NFCWriter()
result = nfc.write_card("2565464", "rajeevan")
nfc.close()