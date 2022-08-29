"""This is the persistence layer module of Bark. It is based on SQLite."""

import sqlite3

from typing import Dict, List, Tuple, Union


class DatabaseManager:
    """This class is used to manage the operations with the DB"""
    
    def __init__(self, database_filename: str) -> None:
        """The DatabaseManager constructor that takes in a filename for the DB"""
        
        self.connection = sqlite3.connect(database_filename)

    def _execute(
        self, 
        statement: str, 
        values: Union[List, Tuple, None] = None
    ) -> sqlite3.Cursor:
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(statement, values or [])
            return cursor

    def create_table(self, table_name: str, columns: Dict[str, str]) -> None:
        columns_with_types = []
        for column_name, column_type in columns.items():
            column_with_type = f"{column_name} {column_type.upper()}"
            columns_with_types.append(column_with_type)
        query = (
            f"CREATE TABLE IF NOT EXISTS {table_name} "
            f"({', '.join(columns_with_types)});"
        )
        self._execute(query)

    def drop_table(self, table_name: str) -> None:
        query = f"DROP TABLE {table_name};"
        self._execute(query)

    def add(self, table_name: str, data: Dict[str, str]) -> None:
        placeholders = ", ".join("?" * len(data))
        column_names = ", ".join(data.keys())
        column_values = tuple(data.values())
        query = (
            f"INSERT INTO {table_name} "
                f"({column_names}) "
            f"VALUES "
                f"({placeholders});"
        )
        self._execute(query, column_values)

    def delete(self, table_name: str, criteria: Dict[str, str]) -> None:
        placeholders = [f"{column} = ?" for column in criteria.keys()]
        delete_criteria = " AND ".join(placeholders)
        criteria_values = tuple(criteria.values())
        query = (
            f"DELETE FROM {table_name} "
            f"WHERE {delete_criteria};"
        )
        self._execute(query, criteria_values)

    def select(
        self, 
        table_name: str, 
        criteria: Union[Dict[str, str], None] = None, 
        order_by: Union[str, None] = None
    ) -> sqlite3.Cursor:
        criteria = criteria or {}
        query = f"SELECT * FROM {table_name}"
        criteria_values = tuple(criteria.values())
        
        if criteria:
            placeholders = [f"{column} = ?" for column in criteria.keys()]
            select_criteria = " AND ".join(placeholders)
            query += f" WHERE {select_criteria}"
        
        if order_by:
            query += f" ORDER BY {order_by}"

        query += ";"

        return self._execute(query, criteria_values)

    def update(
        self,
        table_name: str,
        criteria: Union[Dict[str, str], None] = {},
        data: Union[Dict[str, str], None] = {}
    ):
        placeholders = [f"{column} = ?" for column in criteria.keys()]
        update_criteria = " AND ".join(placeholders)
        
        data_placeholders = ", ".join(f"{key} = ?" for key in data.keys())
        values = tuple(data.values()) + tuple(criteria.values())
        
        self._execute(
            (
                f"UPDATE {table_name} "
                f"SET {data_placeholders} "
                f"WHERE {update_criteria};"
            ),
            values
        )

    def __del__(self) -> None:
        """
            This methods makes it that the DB connection is closed when the DatabaseManager
            instance is deleted (manually or garbage collected)
        """
        self.connection.close()