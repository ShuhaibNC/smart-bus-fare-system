import serial
import time
import threading
import tkinter as tk


class NFCWriter:

    def __init__(self, card_id, fullname, port="COM12", baud=115200):

        self.card_id = card_id
        self.fullname = fullname
        self.port = port
        self.baud = baud
        self.ser = None

    # ---------- connect ----------
    def connect(self):

        print("\nConnecting to ESP32...")

        self.ser = serial.Serial(
            self.port,
            self.baud,
            timeout=1
        )

        time.sleep(2)

        print("Connected.")

    # ---------- close ----------
    def close(self):

        if self.ser and self.ser.is_open:

            self.ser.close()

            print("Serial closed.")

    # ---------- wait ready ----------
    def wait_for_ready(self):

        print("Waiting for READY TO SCAN...")

        start = time.time()

        while time.time() - start < 20:

            if self.ser.in_waiting:

                line = self.ser.readline().decode(
                    errors="ignore"
                ).strip()

                if not line:
                    continue

                print("ESP32:", line)

                # FIX: accept READY TO SCAN
                if "READY TO SCAN" in line.upper():

                    print("READY TO SCAN confirmed")

                    return True

        raise Exception("ESP32 not ready")

    # ---------- send write ----------
    def send_write(self):

        cmd = f"WRITE:{self.card_id}:{self.fullname}\n"

        print("Sending:", cmd.strip())

        self.ser.write(cmd.encode())

    # ---------- listen ----------
    def listen(self):

        print("Waiting for card...")

        start = time.time()

        while time.time() - start < 30:

            if self.ser.in_waiting:

                line = self.ser.readline().decode(
                    errors="ignore"
                ).strip()

                if not line:
                    continue

                print("ESP32:", line)

                if line == "PLACE_CARD":

                    print("👉 Place card on reader")

                elif line == "WRITE_OK":

                    print("✅ WRITE SUCCESS")
                    return True

                elif line.startswith("EXISTING:"):

                    print("⚠ Card has existing data")

                    # automatically overwrite
                    print("Overwriting card...")

                    self.send_write()

                elif line == "CARD_TIMEOUT":

                    print("❌ Card timeout")
                    return False

                elif line == "AUTH_FAIL":

                    print("❌ Authentication failed")
                    return False

        print("Timeout waiting card")

        return False

    # ---------- run ----------
    def run(self):

        try:

            self.connect()

            self.wait_for_ready()

            self.send_write()

            self.listen()

        except Exception as e:

            print("ERROR:", e)

        finally:

            self.close()


# ================= GUI =================

class App:

    def __init__(self, root):

        self.root = root

        self.running = False

        root.title("Smart Bus NFC Writer")

        self.write_btn = tk.Button(
            root,
            text="Update NFC Card",
            font=("Arial", 14),
            width=25,
            command=self.start_write
        )

        self.write_btn.pack(pady=20)

    def start_write(self):

        if self.running:

            print("Already running")
            return

        self.running = True

        self.write_btn.config(state="disabled")

        threading.Thread(
            target=self.write_task,
            daemon=True
        ).start()

    def write_task(self):

        writer = NFCWriter(
            card_id="123456",
            fullname="John Doe"
        )

        writer.run()

        print("Finished")

        self.running = False

        self.write_btn.config(state="normal")


# ================= MAIN =================

if __name__ == "__main__":

    root = tk.Tk()

    app = App(root)

    root.mainloop()