# npt-a
npt a조 백엔드

## Script

- Install Poetry(Window)
    https://python-poetry.org/docs/
- Install Poetry(Linux, MacOS, WSL)
    `curl -sSL https://install.python-poetry.org | python3 -`

- 필요 라이브러리 설치
    `poetry install`

- DB 마이그레이션
    `poetry run python manage.py migrate`

- 개발용 서버 실행
    `poetry run python manage.py runserver`
