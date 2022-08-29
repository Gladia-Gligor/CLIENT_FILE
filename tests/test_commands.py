from unittest import TestCase
from unittest.mock import patch, Mock

from commands import CreateClientsTableCommand, AddClientCommand, ImportGithubStarsCommand


class CreateClientsTableCommandTest(TestCase):
    def setUp(self):
        self.command = CreateClientsTableCommand()

    def test_execute(self):
        with patch("commands.DatabaseManager.create_table") as mocked_create_table:
            self.command.execute()
            mocked_create_table.assert_called_with(
                table_name="clients",
                columns={
                    "id": "integer primary key autoincrement",
                    "client_name": "text not null",
                    "url": "text not null",
                    "notes": "text",
                    "date_added": "text not null",
                }
            )


class AddClientCommandTest(TestCase):
    def setUp(self):
        self.command = AddClientCommand()

    def test_execute(self):
        with patch("commands.DatabaseManager.add") as mocked_add_client:
            data = {
                "client_name": "mock_title",
                "url": "mock_url",
                "notes": "mock_notes"
            }
            result = self.command.execute(data)
            mocked_add_client.assert_called_with(
                table_name="clients",
                data=data
            )
            
            self.assertEqual(result, "Client added!")


class ImportGithubStarsCommandTest(TestCase):
    def setUp(self):
        self.command = ImportGithubStarsCommand()
        self.data = {
            "github_username": "username_foo",
            "preserve_timestamps": True
        }

    def test_execute(self):
        with patch("commands.requests.get") as mocked_get:
            mocked_response = Mock()
            mocked_response.links = {}
            mocked_response.json.return_value = [
                {
                    "starred_at": "2000-01-01T00:00:00Z",
                    "repo": {
                        "name": "name_foo",
                        "html_url": "html_url_foo",
                        "description": "description_foo"
                    }
                }
            ]
            
            mocked_get.return_value = mocked_response
            
            with patch("commands.AddClientCommand.execute") as mocked_add_client:
                mocked_add_client.return_value = "Bookmark added!"
                
                self.command.execute(self.data)
                
                mocked_get.assert_called_with(
                    f"https://api.github.com/users/{self.data['github_username']}/starred",
                    headers = {
                        "Accept": "application/vnd.github.v3.star+json"
                    }
                )
                
                mocked_add_client.assert_called_with(
                    data = {
                        "client_name": "name_foo",
                        "url": "html_url_foo",
                        "notes": "description_foo"
                    },
                    timestamp="2000-01-01T00:00:00"
                )
