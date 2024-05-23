class DatabaseInfo:
    def __init__(self):
        """
        Initializes the DatabaseInfo object with default database connection information.
        """
        # Database URI
        self._DATABASE = 'mysql+pymysql'
        self._USERNAME = 'test'
        self._PASSWORD = '123123'
        self._ADDRESS = '127.0.0.1'
        self._PORT = 3306
        self._DATABASE_NAME = 'airportdb'
        self._CHARSET = 'utf8mb4'

    @property
    def database(self) -> str:
        """
        Gets the database URI.
        :return: Database URI as a string.
        """
        return self._DATABASE

    @database.setter
    def database(self, new_db: str) -> None:
        """
        Sets a new database URI.
        @param new_db: New database URI as a string.
        """
        self._DATABASE = new_db

    @property
    def username(self) -> str:
        """
        Gets the database username.
        :return: Username as a string.
        """
        return self._USERNAME

    @username.setter
    def username(self, new_username: str) -> None:
        """
        Sets a new database username.
        @param new_username: New username as a string.
        """
        self._USERNAME = new_username

    @property
    def password(self) -> str:
        """
        Gets the database password.
        :return: Password as a string.
        """
        return self._PASSWORD

    @password.setter
    def password(self, new_password: str) -> None:
        """
        Sets a new database password.
        @param new_password: New password as a string.
        """
        self._PASSWORD = new_password

    @property
    def address(self) -> str:
        """
        Gets the database server address.
        :return: Address as a string.
        """
        return self._ADDRESS

    @address.setter
    def address(self, new_address: str) -> None:
        """
        Sets a new database server address.
        @param new_address: New address as a string.
        """
        self._ADDRESS = new_address

    @property
    def port(self) -> int:
        """
        Gets the database server port.
        :return: Port as an integer.
        """
        return self._PORT

    @port.setter
    def port(self, new_port: int) -> None:
        """
        Sets a new database server port.
        @param new_port: New port as an integer.
        """
        self._PORT = new_port

    @property
    def database_name(self) -> str:
        """
        Gets the name of the database.
        :return: Database name as a string.
        """
        return self._DATABASE_NAME

    @database_name.setter
    def database_name(self, new_db_name: str) -> None:
        """
        Sets a new database name.
        @param new_db_name: New database name as a string.
        """
        self._DATABASE_NAME = new_db_name

    @property
    def charset(self) -> str:
        """
        Gets the database character set.
        :return: Character set as a string.
        """
        return self._CHARSET

    @charset.setter
    def charset(self, new_charset: str) -> None:
        """
        Sets a new database character set.
        @param new_charset: New character set as a string.
        """
        self._CHARSET = new_charset
