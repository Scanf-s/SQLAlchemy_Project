# 프로젝트 타이틀

이 프로젝트는 MySQL 데이터베이스에 대한 더미 데이터 생성을 위한 스크립트를 개발하는 과정을 담고 있습니다. 
각 주차별 과제를 통해 점진적으로 기능을 확장해 나가며, Python과 SQLAlchemy, Faker 같은 라이브러리를 활용합니다.

### 필수 조건

- Python ^3.10
- MySQL 데이터베이스 서버

### 설치

1. 이 저장소를 클론합니다:
```bash
git clone [repo-link]
```

2. 필요한 Python 라이브러리를 설치합니다:
```bash
poetry install
```

3. MySQL에서 `airport-ddl.sql` 스크립트를 실행하여 데이터베이스와 테이블을 생성합니다.

### 실행

프로젝트를 실행하기 위해 다음 명령어를 사용합니다:
```bash
poetry shell
poetry run python src/app.py
```

## 과제 개요

### 1주차 과제: 테스트를 위한 더미 데이터 만들기

- **기간**: 4월 17일 ~ 4월 24일
- **목표**: MySQL 데이터베이스에 14개의 테이블에 대한 더미 데이터 생성
- **상황**:
  - MySQL 데이터베이스에 14개 테이블 생성 완료
  - 각 테이블에 1,000개에서 20,000개 사이의 더미 데이터 필요

### 2주차 과제: 더미 데이터 생성 로직 공통화

- **기간**: 4월 24일 ~ 5월 1일
- **목표**: 반복적인 더미 데이터 생성 작업을 공통화하여 효율성 증대
- **상황**:
  - 새로운 테이블 10개 추가
  - 공통화된 접근 방식 필요

### 3주차 과제: MySQL DB 관리 도구 개발

- **기간**: 이어지는 1주
- **목표**: 데이터베이스 관리 기능을 자동화하는 도구 개발
- **필수 구현 요건**:
  - 여러 DB 접속 정보 관리
  - 스키마, 테이블, 뷰 정보 조회 기능
  - DDL 스크립트 생성 기능

## 사용된 도구

- [Poetry](https://python-poetry.org/) - 의존성 관리 및 패키지 관리자
- [SQLAlchemy](https://www.sqlalchemy.org/) - 데이터베이스 관리
- [Faker](https://faker.readthedocs.io/en/master/) - 더미 데이터 생성