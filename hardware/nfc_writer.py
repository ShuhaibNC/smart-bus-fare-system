import serial
import time

class NFCWriter:
    def __init__(self, port="COM12", baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=3)
        time.sleep(2)

    def send_cmd(self, cmd):
        self.ser.reset_input_buffer()
        self.ser.write((cmd + "\n").encode())
        return self.ser.readline().decode().strip()

    def check_card(self):
        return self.send_cmd("CHECK")

    def delete_card(self):
        return self.send_cmd("DELETE")

    def write_card(self, student_id, name):
        return self.send_cmd(f"WRITE:{student_id}|{name}")

    def close(self):
        self.ser.close()
