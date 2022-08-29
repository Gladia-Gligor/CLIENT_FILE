import sqlite3

from unittest import TestCase
from unittest.mock import patch

from database import DatabaseManager


class CreateDatabaseTableTest(TestCase):
    def setUp(self):
        self.db = DatabaseManager(":memory:")
    
    def test_create_table(self):
        with patch("database.DatabaseManager._execute") as mocked_execute:
            self.db.create_table(
                table_name="test_table",
                columns={
                    "id": "integer primary key autoincrement",
                    "test_column_one": "text not null",
                    "test_column_two": "text not null"
                }
            )
            mocked_execute.assert_called_with(
                (
                    "CREATE TABLE IF NOT EXISTS test_table "
                    "(id INTEGER PRIMARY KEY AUTOINCREMENT, test_column_one TEXT NOT NULL, test_column_two TEXT NOT NULL);"
                )
            )

    def test_missing_table_name(self):
        with self.assertRaises(sqlite3.OperationalError):
            self.db.create_table(
                table_name="",
                columns={
                    "id": "integer primary key autoincrement",
                    "test_column_one": "text not null",
                    "test_column_two": "text not null"
                }
            )

    def tearDown(self):
        del self.db


class DropDatabaseTableTest(TestCase):
    def setUp(self):
        self.db = DatabaseManager(":memory:")

    def test_drop_table(self):
        with patch("database.DatabaseManager._execute") as mocked_execute:
            self.db.drop_table(table_name="test_table")
            mocked_execute.assert_called_with("DROP TABLE test_table;")

    def tearDown(self):
        del self.db


class AddEntryToTableTest(TestCase):
    def setUp(self):
        self.db = DatabaseManager(":memory:")

    def test_add_entry(self):
        with patch("database.DatabaseManager._execute") as mocked_execute:
            self.db.add(
                table_name="test_table",
                data={
                    "key_one": "value_one",
                    "key_two": "value_two"
                }
            )
            mocked_execute.assert_called_once_with(
                "INSERT INTO test_table (key_one, key_two) VALUES (?, ?);", 
                ("value_one", "value_two")
            )

    def tearDown(self):
        del self.db


class SelectEntryFromTableTest(TestCase):
    def setUp(self):
        self.db = DatabaseManager(":memory:")

    def test_select_entry(self):
        with patch("database.DatabaseManager._execute") as mocked_execute:
            self.db.select(
                table_name="test_table",
            )
            mocked_execute.assert_called_once_with(
                "SELECT * FROM test_table;", ()
            )

    def test_select_entry_with_criteria(self):
        with patch("database.DatabaseManager._execute") as mocked_execute:
            self.db.select(
                table_name="test_table",
                criteria={
                    "key_one": "value_one",
                    "key_two": "value_two"
                },
            )
            mocked_execute.assert_called_once_with(
                "SELECT * FROM test_table WHERE key_one = ? AND key_two = ?;",
                ("value_one", "value_two")
            )

    def test_select_entry_with_criteria_ordered(self):
        with patch("database.DatabaseManager._execute") as mocked_execute:
            self.db.select(
                table_name="test_table",
                criteria={
                    "key_one": "value_one",
                    "key_two": "value_two"
                },
                order_by="key_one"
            )
            mocked_execute.assert_called_once_with(
                "SELECT * FROM test_table WHERE key_one = ? AND key_two = ? ORDER BY key_one;",
                ("value_one", "value_two")
            )

    def tearDown(self):
        del self.db


class DeleteEntryFromTableTest(TestCase):
    def setUp(self) -> None:
        self.db = DatabaseManager(":memory:")

    def test_delete_entry(self):
        with patch("database.DatabaseManager._execute") as mocked_execute:
            self.db.delete(
                table_name="test_table",
                criteria={
                    "key_one": "value_one",
                    "key_two": "value_two"
                }
            )
            mocked_execute.assert_called_once_with(
                "DELETE FROM test_table WHERE key_one = ? AND key_two = ?;",
                ("value_one", "value_two")
            )

    def test_delete_entry_missing_criteria(self):
        with patch("database.DatabaseManager._execute"):
            with self.assertRaises(TypeError):
                self.db.delete(
                    table_name="test_table",
                )

    def tearDown(self) -> None:
        del self.db