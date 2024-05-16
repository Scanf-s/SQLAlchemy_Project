from sqlalchemy import create_engine
from util.error.error_handler import exception_handler


@exception_handler
def create_engine_connection(db_info):
    """
    MySQL 초기화를 위한 연결 엔진을 생성한다.
    연결에 실패할 경우, 에러 메시지를 출력한다.
    :return: 성공적으로 생성된 연결 엔진 객체를 반환한다.
    :raises Exception: 연결 생성 중 오류가 발생한 경우 예외를 발생시킨다.
    """
    engine_connection_string = (
        f'{db_info.database}://root:123123@'
        f'{db_info.address}:{db_info.port}'
    )
    engine = create_engine(
        engine_connection_string,
        echo=False
    )
    return engine


@exception_handler
def create_database_connection(db_info):
    """
    MySQL 데이터베이스에 연결하기 위한 데이터베이스 엔진을 생성한다.
    이 함수는 SQLAlchemy의 create_engine 함수를 사용하여 MySQL 데이터베이스에 연결하기 위한 엔진을 생성한다.
    연결에 실패할 경우, 에러 메시지를 출력한다.
    :return: 성공적으로 생성된 연결 엔진 객체를 반환한다.
    :raises Exception: 연결 생성 중 오류가 발생한 경우 예외를 발생시킨다.
    """
    database_connection_string = (
        f'{db_info.database}://{db_info.username}:{db_info.password}@'
        f'{db_info.address}:{db_info.port}/{db_info.database_name}?'
        f'charset={db_info.charset}'
    )

    engine = create_engine(
        database_connection_string,
        echo=False
    )
    return engine
