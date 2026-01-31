import serial
import time


class NFCWriter:
    def __init__(self, card_id, fullname, port="COM12", baud=115200):
        self.card_id = card_id
        self.fullname = fullname
        self.port = port
        self.baud = baud
        self.ser = None

    def connect(self):
        self.ser = serial.Serial(self.port, self.baud, timeout=1)
        time.sleep(2)

    def wait_for_ready(self):
        print("Waiting for READY...")
        while True:
            if self.ser.in_waiting:
                line = self.ser.readline().decode(errors="ignore").strip()
                print("ESP32:", line)
                if line == "READY":
                    break

    def send_write(self):
        time.sleep(0.5)
        print("Sending WRITE command...")
        cmd = f"WRITE:{self.card_id}:{self.fullname}\n"
        self.ser.write(cmd.encode())

    def listen(self):
        while True:
            if self.ser.in_waiting:
                line = self.ser.readline().decode(errors="ignore").strip()
                print("ESP32:", line)

                if line == "PLACE_CARD":
                    print("👉 Place card now")

                if line == "WRITE_OK":
                    print("✅ WRITE SUCCESS")
                    break

                if line.startswith("EXISTING:"):
                    print("⚠️ CARD HAS DATA:", line)
                    break

    def run(self):
        self.connect()
        self.wait_for_ready()
        self.send_write()
        self.listen()


# Example usage
# writer = NFCWriter(card_id="123456", fullname="John Doe")
# writer.run()
