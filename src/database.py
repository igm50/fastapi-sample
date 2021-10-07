from os import name
from typing import List, Optional
from MySQLdb.connections import Connection
import pymysql

from model import City


class Database:
    def __init__(self):
        self.con = None

    def __enter__(self):
        self.con = pymysql.connect(
            host="database", port=3306, db="world", user="root", password="password", charset="utf8")
        return self

    def __exit__(self, exec_type, exec_value, traceback):
        self.con.close()

    def read_cities(self, limit: Optional[int]) -> List[City]:
        with self as db, db.con.cursor() as cursor:
            if type(limit) == int:
                cursor.execute(self.__select_city__() + "LIMIT %s", limit)
            else:
                cursor.execute(self.__select_city__)
            results = cursor.fetchall()

        return [self.__to_city__(result) for result in results]

    def read_city(self, city_id: int) -> City:
        with self as db, db.con.cursor() as cursor:
            sql = self.__select_city__() + "WHERE `id` =%s"
            cursor.execute(sql, city_id)
            result = cursor.fetchone()

        return self.__to_city__(result)

    @staticmethod
    def __select_city__() -> str:
        return "SELECT `id`, `name`, `countryCode`, `district`, `population` FROM `city`"

    @staticmethod
    def __to_city__(result):
        return City(id=result[0], name=result[1], country_code=result[2], district=result[3], population=result[4])
