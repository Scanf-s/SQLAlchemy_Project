# Database URI
DATABASE = 'mysql+pymysql'
USERNAME = 'test'
PASSWORD = '123123'
# Change address from 127.0.0.1 to db (compose.yaml)
ADDRESS = 'localhost'
PORT = 3306
DATABASE_NAME = 'airportdb'
CHARSET = 'utf8mb4'


# wsl2 ubuntu에서 mysql설정하는 방법
# https://yogingang.tistory.com/13
# https://stackoverflow.com/questions/39281594/error-1698-28000-access-denied-for-user-rootlocalhost
# 반드시 두 링크를 참고하자
# 1. 계정을 생성하고, 권한을 부여한다
# 2. /etc/mysql~~~~/mysqld.cnf에
# port = 3306 주석된거 해제하고, user = mysql로 되어있는거 생성한 계정이름으로 바꾸니까
# python에서 접속 가능해졌음
# 이거 해결하느라 3시간 걸림;;;;;;;;;;;;;;;;;;;;