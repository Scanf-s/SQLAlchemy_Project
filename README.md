# 더미데이터 생성 API

### 개발 환경 및 사용 기술
![](https://img.shields.io/badge/Ubuntu-24292e?style=flat&logo=Ubuntu&logoColor=white")
![](https://img.shields.io/badge/Poetry-24292e?style=flat&logo=Poetry&logoColor=white")
![](https://img.shields.io/badge/Python-24292e?style=flat&logo=Python&logoColor=white")
![](https://img.shields.io/badge/SQLAlchemy-24292e?style=flat&logo=SQLAlchemy&logoColor=white")
![](https://img.shields.io/badge/Flask-24292e?style=flat&logo=Flask&logoColor=white")

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
```
(Or modify the root password in config/database_engines.py's create_engine_connection())

```mysql
create user 'test'@'localhost' identified by '123123';
```
(Or modify the _USERNAME and _PASSWORD in config/DatabaseInfo.py)

#### 3. Open the Project with Your IDE and Install Poetry
In your IDE console
```bash
pip install poetry
poetry config virtualenvs.in-project true
poetry config virtualenvs.path "./.venv"
poetry install
```

#### 4. Register Google API application
[Register your google API application here](https://console.cloud.google.com/welcome)
[Google Developer docs for Korean](https://developers.google.com/identity/protocols/oauth2/service-account?hl=ko#creatinganaccount)
[Reference blog for Korean](https://goldenrabbit.co.kr/2023/08/07/oauth%EB%A5%BC-%EC%82%AC%EC%9A%A9%ED%95%9C-%EA%B5%AC%EA%B8%80-%EB%A1%9C%EA%B7%B8%EC%9D%B8-%EC%9D%B8%EC%A6%9D%ED%95%98%EA%B8%B0-1%ED%8E%B8/)

Then, modify config/GoogleAPIKey.json
```json
{
  "CLIENT_KEY": "your_google_api_client_key",
  "SECRET_KEY": "your_google_api_secret_key"
}
```

#### 5. Run Flask project
```bash
poetry shell
flask run
```

#### 6. Open your browser
- Connect to `127.0.0.1:5000`
