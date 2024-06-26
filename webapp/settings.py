import os
import yaml
from dataclasses import dataclass, field


@dataclass()
class ServerData():
    port: int = 8080
    session_secret_key: str = ''
    session_timeout: int = 2678400
    debug_mode: bool = False
    app_name: str = 'PyBeetle'


class Server(ServerData):
    """Structre storing all the server settings"""
    def __init__(self, data=None):
        if data is None:
            data = {}
        data = {k: data[k] for k in ServerData.__dataclass_fields__.keys() if k in data}
        super().__init__(**data)
        if self.session_secret_key == '':
            raise "Server must have the session_secret_key value set"



@dataclass()
class DatabaseData():
    type: str = ''
    server: str = ''
    username: str = ''
    password: str = ''
    database: str =''
    file_path: str = ''


DATABASE_TYPES: list = ['sqlite', 'mssql', 'postgresql', 'mysql']


class Database(DatabaseData):
    """Structure storing all the datbase settings"""
    def __init__(self, data=None):
        if data is None:
            data = {}
        data = {k: data[k] for k in DatabaseData.__dataclass_fields__.keys() if k in data}
        super().__init__(**data)
        # Check if correct database type is set
        self.type = self.type.lower()
        if not self.type in DATABASE_TYPES:
            raise f"Not valid Database type set: {self.type} Type must be one of: {", ".join(DATABASE_TYPES)}"
        if self.type == 'sqlite' and self.file_path == '':
            raise "Database type sqlite requirs a file path be set"
        if self.type in ['mssql', 'postgresql', 'mysql']:
            if self.server == '':
                raise "Database types of: 'mssql', 'postgresql', 'mysql' \nMust have the server value set."
            if self.database == '':
                raise "Database types of: 'mssql', 'postgresql', 'mysql' \nMust have the database value set."
            if self.username == '':
                raise "Database types of: 'mssql', 'postgresql', 'mysql' \nMust have the username value set."
            if self.password == '':
                raise "Database types of: 'mssql', 'postgresql', 'mysql' \nMust have the password value set."



@dataclass
class SettinngsData():
    server: Server = field(default_factory=Server)
    database: Database = field(default_factory=Database)


class Settings(SettinngsData):
    """Structure storing all the config settings"""
    def __init__(self):
        self._data = {}

    def is_loaded(self):
        """Check if settings has been loaded or not.
        
        Return:
        true if loaded else false
        """
        return bool(self._data)

    def load_settings(self, file_path: str =''):
        """
        Create the settings structure
        
        arguments:
        file_path - Path to the yaml file to read
        """
        if file_path == '' or file_path is None or not file_path.endswith('.yaml') and not file_path.endswith('.yml'):
            raise f"Invalid file path supply for settings: {file_path}"
        if not os.access(file_path, os.R_OK):
            raise f"Unable to read file: {file_path}"
        
        with open(file_path, 'r') as file:
            self._data = yaml.safe_load(file)
        self._data = {k: self._data[k] for k in SettinngsData.__dataclass_fields__.keys() if k in self._data}
        super().__init__(**self._data)
        if isinstance(self.server, dict):
            self.server = Server(self.server)
        if isinstance(self.database, dict):
            self.database = Database(self.database)
