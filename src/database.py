from typing import Optional
from MySQLdb.connections import Connection
import pymysql

from model import City


class Database:
    con: Connection

    def connect(self):
        self.con = pymysql.connect(
            host="database", port=3306, db="world", user="root", password="password", charset="utf8")

    def close(self):
        self.con.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        self.close()

    def read_cities(self, limit: Optional[int]) -> City:
        with self as db:
            with db.con.cursor() as cursor:
                base_sql = "SELECT * FROM `city`"
                limit_sql = "LIMIT %s"
                if type(limit) == int:
                    cursor.execute(base_sql + limit_sql, limit)
                else:
                    cursor.execute(base_sql)
                results = cursor.fetchall()

        return [City(result[0], result[1], result[2], result[3], result[4]) for result in results]

    def read_city(self, city_id: int) -> City:
        with self as db:
            with db.con.cursor() as cursor:
                sql = "SELECT * FROM `city` WHERE `id` =%s"
                cursor.execute(sql, city_id)
                result = cursor.fetchone()
                city = City(result[0], result[1],
                            result[2], result[3], result[4])

        return city
