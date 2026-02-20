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
            database=DB_NAME,
            autocommit=True
        )

        self.cursor = self.db.cursor()

        self.last_uid = None
        self.last_scan_time = 0


    # ---------- connect serial ----------
    def connect_serial(self):

        try:

            self.ser = serial.Serial(
                SERIAL_PORT,
                BAUD_RATE,
                timeout=1
            )

            time.sleep(2)

            print("READY TO SCAN...")

        except Exception as e:

            print("SERIAL ERROR:", e)

            exit()


    # ---------- get student ----------
    def get_student(self, card_id):

        sql = """
        SELECT username, balance, status
        FROM student_studentnfccard
        WHERE card_id=%s
        """

        self.cursor.execute(sql, (card_id,))

        return self.cursor.fetchone()


    # ---------- get student route ----------
    def get_student_route(self, username):

        sql = """
        SELECT stop1, stop2
        FROM student_busroute
        WHERE LOWER(TRIM(user)) = LOWER(TRIM(%s))
        """

        self.cursor.execute(sql, (username,))

        return self.cursor.fetchone()


    # ---------- get monthly bus fee ----------
    def get_bus_fee(self, dest_stop):

        sql = """
        SELECT busfee
        FROM system_admin_busfee
        WHERE LOWER(TRIM(dest_stop)) = LOWER(TRIM(%s))
        """

        self.cursor.execute(sql, (dest_stop,))

        result = self.cursor.fetchone()

        if result:
            return float(result[0])

        return None


    # ---------- get today's tap count ----------
    def get_today_tap_count(self, card_id):

        sql = """
        SELECT COUNT(*)
        FROM bus_log
        WHERE card_id=%s AND tap_date=%s
        """

        today = datetime.now().date()

        self.cursor.execute(sql, (card_id, today))

        result = self.cursor.fetchone()

        return result[0]


    # ---------- update balance ----------
    def update_balance(self, card_id, new_balance):

        sql = """
        UPDATE student_studentnfccard
        SET balance=%s
        WHERE card_id=%s
        """

        self.cursor.execute(sql, (new_balance, card_id))


    # ---------- save log ----------
    def save_log(self, card_id, username):

        now = datetime.now()

        sql = """
        INSERT INTO bus_log
        (card_id, student_name, tap_date, tap_time, location)
        VALUES (%s, %s, %s, %s, %s)
        """

        self.cursor.execute(sql, (
            card_id,
            username,
            now.date(),
            now.time(),
            LOCATION
        ))


    # ---------- process card ----------
    def process_card(self, card_id):

        now = time.time()

        # prevent duplicate scan within 2 seconds
        if card_id == self.last_uid and now - self.last_scan_time < 2:
            return

        self.last_uid = card_id
        self.last_scan_time = now


        # ---------- get student ----------
        student = self.get_student(card_id)

        if not student:

            print("CARD NOT REGISTERED")

            return


        username, balance, status = student

        balance = float(balance)


        # ---------- check blocked ----------
        if status.lower() == "blocked":

            print(f"{username} CARD BLOCKED")

            return


        # ---------- check daily tap limit ----------
        tap_count = self.get_today_tap_count(card_id)

        if tap_count >= 2:

            print(f"{username} DAILY LIMIT REACHED")

            return


        # ---------- get route ----------
        route = self.get_student_route(username)

        if not route:

            print(f"{username} ROUTE NOT FOUND")

            return


        stop1, stop2 = route


        # ---------- get monthly fee ----------
        monthly_fee = self.get_bus_fee(stop2)

        if monthly_fee is None:

            print(f"FEE NOT FOUND FOR STOP {stop2}")

            return


        # ---------- calculate per tap deduction ----------
        fee = round(monthly_fee / 30 / 2, 2)


        # ---------- check balance ----------
        if balance < fee:

            print(f"{username} INSUFFICIENT BALANCE: {balance}")

            return


        # ---------- deduct balance ----------
        new_balance = round(balance - fee, 2)


        # ---------- update database ----------
        self.update_balance(card_id, new_balance)


        # ---------- save log ----------
        self.save_log(card_id, username)


        # ---------- print success ----------
        print(f"{username} | Tap {tap_count+1}/2 | Fee: {fee} | Balance: {new_balance}")


    # ---------- listen ----------
    def listen(self):

        while True:

            try:

                if self.ser.in_waiting:

                    line = self.ser.readline().decode(errors="ignore").strip()

                    if line.startswith("CARD:"):

                        parts = line.split(":")

                        if len(parts) >= 2:

                            card_id = parts[1]

                            self.process_card(card_id)

                time.sleep(0.05)

            except Exception as e:

                print("ERROR:", e)

                time.sleep(1)


# ---------- MAIN ----------
if __name__ == "__main__":

    scanner = BusScanner()

    scanner.connect_serial()

    scanner.listen()