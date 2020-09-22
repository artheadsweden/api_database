import json
import sqlite3

import requests
import time

class Advice:
    def __init__(self, id=0, advice="", slip=None):
        if slip is not None:
            if not slip.text.endswith("}}"):
                adv_text = slip.text + "}"
                slip = json.loads(adv_text)
            else:
                slip = slip.json()
            self.id = slip["slip"]["id"]
            self.advice = slip["slip"]["advice"]
        else:
            self.id = id
            self.advice=advice

    def __str__(self):
        return f"The advice with id {self.id}:\n{self.advice}"

    def as_tuple(self):
        return int(self.id), self.advice, int(self.id)


class Slip:
    def __init__(self):
        self.url = "https://api.adviceslip.com/advice"

    def get_new_advice(self, id_str=""):
        sql = """
            INSERT INTO advice(id, the_advice) 
             SELECT ?, ?
             WHERE NOT EXISTS(SELECT 1 FROM advice WHERE id = ?)
        """
        connection = self.connect_database()

        cursor = connection.cursor()
        url = self.url + ("" if not id_str else f"/{id_str}")
        resp = requests.get(url)

        json_answer = resp.json()
        if "message" in json_answer:
            if json_answer["message"]["type"] == "error":
                print("Item not found")
                return None
        adv = Advice(slip=resp)
        cursor.execute(sql, adv.as_tuple())
        connection.commit()

        connection.close()
        return adv

    def connect_database(self):
        database = "advice.db"

        connection = None

        try:
            connection = sqlite3.connect(database)
            print(f"Connected to SqlLite version {sqlite3.version}")
            sql = """
                    CREATE TABLE IF NOT EXISTS advice (
                        id INTEGER PRIMARY KEY,
                        the_advice TEXT NOT NULL
                    )
                """
            cursor = connection.cursor()
            cursor.execute(sql)
            return connection
        except sqlite3.Error as e:
            print(e)
            return None

    def get_advice_by_id(self, id):
        connection = self.connect_database()
        sql = """
            SELECT the_advice FROM advice WHERE id = ?
        """
        cursor = connection.cursor()
        cursor.execute(sql, (int(id), ))
        advice = cursor.fetchone()
        connection.close()

        if advice is None:
            print("From API")
            adv = self.get_new_advice(id)
        else:
            print("From DB")
            advice = advice[0]
            adv = Advice(id=id, advice=advice)
        return adv


def main():
    slip = Slip()
    advice = slip.get_advice_by_id(250)
    if advice is not None:
        print(advice)



if __name__ == '__main__':
    main()
