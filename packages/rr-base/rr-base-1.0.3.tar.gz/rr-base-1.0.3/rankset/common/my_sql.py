import mysql.connector
import pandas as pd


class MySqlConnection:

    def __init__(self, user='root', password='password', host='127.0.0.1', database='sys'):
        self.__connection = mysql.connector.connect(user=user, password=password,
                                                    host=host,
                                                    database=database)
        self.__cursor_connection = self.__connection.cursor()
        self.__data_result = None

    def get_data(self, query, return_data_frame: bool = False, close_connection=False):
        try:
            self.__cursor_connection.execute(query)
            self.__data_result = list(self.__cursor_connection.fetchall())
            if close_connection:
                self.close_connection()
            if not return_data_frame:
                return self.__data_result, self.__cursor_connection.column_names
            else:
                return pd.DataFrame(data=self.__data_result, columns=self.__cursor_connection.column_names)
        except Exception as e:
            print(e)

    def manipulate_data(self, query, data=None, is_list=True, delete_data=False, close_connection=False):
        try:
            if is_list and not delete_data:
                self.__cursor_connection.executemany(query, data)
            elif not delete_data:
                self.__cursor_connection.execute(query, data)
            else:
                self.__cursor_connection.execute(query)

            self.__connection.commit()
            if close_connection:
                self.close_connection()
        except Exception as e:
            self.close_connection()
            raise print(e)

    def close_connection(self):
        try:
            self.__connection.close()
        except Exception as e:
            raise print(e)
