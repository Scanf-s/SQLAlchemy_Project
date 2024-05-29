# 더미데이터 생성 API

### 개발 환경 및 사용 기술
![](https://img.shields.io/badge/Ubuntu-E95420?style=flat&logo=Ubuntu&logoColor=white")
![](https://img.shields.io/badge/Poetry-60A5FA?style=flat&logo=Poetry&logoColor=white")
![](https://img.shields.io/badge/Python-3776AB?style=flat&logo=Python&logoColor=white")
![](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat&logo=SQLAlchemy&logoColor=white")
![](https://img.shields.io/badge/Flask-000000?style=flat&logo=Flask&logoColor=white")

### 프로젝트 구조
```text
.
├── README.md
├── app.py
├── config
│   ├── __init__.py
│   ├── db.py
│   └── db_info.py
├── models
│   └── airport-ddl.sql
├── requirements.txt
├── ui
│   ├── __init__.py
│   └── user_interface.py
└── util
    ├── __init__.py
    ├── database_utils.py
    ├── dummy_generators.py
    ├── error
    │   ├── __init__.py
    │   └── error_handler.py
    └── utils.py
```

### 설치 방법

#### 1. Clone repository
```bash
git clone [this repository]
```

#### 2. Install MySQL
[Ubuntu MySQL](https://ubuntu.com/server/docs/install-and-configure-a-mysql-server)

```bash
sudo apt install mysql-server
sudo service mysql start
```

```mysql
mysql -u root -p 123123
(Or modify config/database_engines.py 'create_engine_connection()'s root password for you'

create user 'test'@'localhost' identified by '123123';
(Or modify config/DatabaseInfo.py class '_USERNAME', '_PASSWORD' for you)
```

#### 3. Open project with your IDE, Install Poetry

In your IDE console
```bash
pip install poetry
poetry config virtualenvs.in-project true
poetry config virtualenvs.path "./.venv"
poetry install
```

#### 4. Run Flask project
```bash

```

### 과제 개요

#### 1주차 과제: 테스트를 위한 더미 데이터 만들기

- **기간**: 4월 17일 ~ 4월 24일
- **목표**: MySQL 데이터베이스에 14개의 테이블에 대한 더미 데이터 생성
- **상황**:
  - MySQL 데이터베이스에 14개 테이블 생성 완료
  - 각 테이블에 1,000개에서 20,000개 사이의 더미 데이터 필요

#### 2주차 과제: 더미 데이터 생성 로직 공통화

- **기간**: 4월 24일 ~ 5월 1일
- **목표**: 반복적인 더미 데이터 생성 작업을 공통화하여 효율성 증대
- **상황**:
  - 새로운 테이블 10개 추가
  - 공통화된 접근 방식 필요

#### 3주차 과제: MySQL DB 관리 도구 개발

- **기간**: 5월 8일 ~ 5월 20일
- **목표**: 데이터베이스 관리 기능을 자동화하는 도구 개발
- **필수 구현 요건**:
  - 여러 DB 접속 정보 관리
  - 스키마, 테이블, 뷰 정보 조회 기능
  - DDL 스크립트 생성 기능
