class DatabaseInfo:
    def __init__(self):
        # Database URI
        self._DATABASE = 'mysql+pymysql'
        self._USERNAME = 'test'
        self._PASSWORD = '123123'
        # Change address from 127.0.0.1 to db (compose.yaml)
        self._ADDRESS = '127.0.0.1'
        self._PORT = 3306
        self._DATABASE_NAME = 'airportdb'
        self._CHARSET = 'utf8mb4'

        # wsl2 ubuntu에서 mysql설정하는 방법
        # https://yogingang.tistory.com/13
        # https://stackoverflow.com/questions/39281594/error-1698-28000-access-denied-for-user-rootlocalhost
        # 반드시 두 링크를 참고하자
        # 1. 계정을 생성하고, 권한을 부여한다
        # 2. /etc/mysql~~~~/mysqld.cnf에
        # port = 3306 주석된거 해제하고, user = mysql로 되어있는거 생성한 계정이름으로 바꾸니까
        # python에서 접속 가능해졌음

    # @property : python의 getter
    # @함수명.setter : python의 setter
    @property
    def database(self):
        return self._DATABASE

    @database.setter
    def database(self, new_db):
        self._DATABASE = new_db

    @property
    def username(self):
        return self._USERNAME

    @username.setter
    def username(self, new_username):
        self._USERNAME = new_username

    @property
    def password(self):
        return self._PASSWORD

    @password.setter
    def password(self, new_password):
        self._PASSWORD = new_password

    @property
    def address(self):
        return self._ADDRESS

    @address.setter
    def address(self, new_address):
        self._ADDRESS = new_address

    @property
    def port(self):
        return self._PORT

    @port.setter
    def port(self, new_port):
        self._PORT = new_port

    @property
    def database_name(self):
        return self._DATABASE_NAME

    @database_name.setter
    def database_name(self, new_db_name):
        self._DATABASE_NAME = new_db_name

    @property
    def charset(self):
        return self._CHARSET

    @charset.setter
    def charset(self, new_charset):
        self._CHARSET = new_charset
