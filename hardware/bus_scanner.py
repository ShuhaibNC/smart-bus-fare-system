import serial
import time
import pymysql
from datetime import datetime


# -------- CONFIG --------

SERIAL_PORT = "COM12"
BAUD_RATE = 115200

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "123"
DB_NAME = "sbfs"

LOCATION = "BUS_01"


class BusScanner:

    def __init__(self):

        self.ser = None

        self.db = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        self.cursor = self.db.cursor()

        self.last_uid = None
        self.last_scan_time = 0


    # ---------- connect serial ----------
    def connect_serial(self):

        self.ser = serial.Serial(
            SERIAL_PORT,
            BAUD_RATE,
            timeout=1
        )

        time.sleep(2)

        print("READY TO SCAN...")


    # ---------- get tap count ----------
    def get_tap_count(self, card_id):

        today = datetime.now().strftime("%Y-%m-%d")

        sql = """
        SELECT COUNT(*) FROM bus_log
        WHERE card_id=%s AND tap_date=%s
        """

        self.cursor.execute(sql, (card_id, today))

        result = self.cursor.fetchone()

        return result[0]


    # ---------- save tap ----------
    def save_tap(self, card_id, name):

        now = datetime.now()

        date = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")

        sql = """
        INSERT INTO bus_log
        (card_id, student_name, tap_date, tap_time, location)
        VALUES (%s, %s, %s, %s, %s)
        """

        self.cursor.execute(sql, (
            card_id,
            name,
            date,
            time_str,
            LOCATION
        ))

        self.db.commit()


    # ---------- process card ----------
    def process_card(self, card_id, name):

        now = time.time()

        # prevent instant duplicate reads
        if card_id == self.last_uid and now - self.last_scan_time < 2:
            return

        self.last_uid = card_id
        self.last_scan_time = now

        tap_count = self.get_tap_count(card_id)

        if tap_count >= 2:

            print("INVALID")
            return

        # save tap
        self.save_tap(card_id, name)

        # print ONLY name
        print(name)


    # ---------- listen ----------
    def listen(self):

        while True:

            if self.ser.in_waiting:

                line = self.ser.readline().decode(
                    errors="ignore"
                ).strip()

                if line.startswith("CARD:"):

                    parts = line.split(":")

                    if len(parts) >= 3:

                        card_id = parts[1]
                        name = parts[2]

                        self.process_card(card_id, name)

            time.sleep(0.05)


# ---------- MAIN ----------
if __name__ == "__main__":

    scanner = BusScanner()

    scanner.connect_serial()

    scanner.listen()