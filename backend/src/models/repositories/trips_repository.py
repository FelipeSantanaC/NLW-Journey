from typing import Dict
from sqlite3 import Connection

class TripsRepository:
    def __init__(self, conn: Connection) -> None:
        self.__conn = conn
    
    def create_trip(self, trips_infos: Dict):
        cursor = self.__conn.cursor()
        cursor.execute(
            '''
                INSERT INTO trips
                    (id, destination, start_date, end_date, owner_name, owner_email)
            '''
        )