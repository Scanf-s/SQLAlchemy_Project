from sqlalchemy import create_engine
from src.config.db_info import (
    DATABASE,
    USERNAME,
    PASSWORD,
    ADDRESS,
    PORT,
    DATABASE_NAME,
    CHARSET
)


def create_connection():

    """
    MySQL 데이터베이스에 연결하기 위한 엔진을 생성한다.

    이 함수는 SQLAlchemy의 create_engine 함수를 사용하여 MySQL 데이터베이스에 연결하기 위한 엔진을 생성한다.
    연결에 실패할 경우, 에러 메시지를 출력한다.

    :return: 성공적으로 생성된 연결 엔진 객체를 반환한다.
    :raises Exception: 연결 생성 중 오류가 발생한 경우 예외를 발생시킨다.
    """

    try:
        engine = create_engine(
            f'{DATABASE}://{USERNAME}:{PASSWORD}@{ADDRESS}:{PORT}/{DATABASE_NAME}?charset={CHARSET}',
            echo=False
        )
        return engine
    except Exception as e:
        print(f"ERROR: {e}")
        raise  # 발생한 예외를 다시 발생시켜 호출자가 처리하도록 한다.
