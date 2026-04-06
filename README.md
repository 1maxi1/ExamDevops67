# ExamDevops6 - Билет 21

REST API-приложение для проверки баланса проездного билета и получения информации об изменениях движения в метро.

## Что реализовано

- веб-сервер на FastAPI;
- база данных PostgreSQL;
- начальные данные из билета;
- публичный endpoint для получения изменений в метро;
- защищенный endpoint для получения баланса по паре `телефон + SMS-код`;
- возврат станции последнего прохода через турникет;
- Dockerfile и `docker-compose.yml`;
- тесты, линтер и SAST-проверка;
- конфигурация TeamCity DSL для `main` и `feature/fix` веток.

## API

### Проверка работоспособности

```http
GET /health
```

### Получение изменений в метро

```http
GET /api/v1/metro/changes
```

Пример ответа:

```json
[
  {
    "id": 1,
    "description": "Закрытие станции Рижская",
    "affected_line": "Калужско-рижская"
  }
]
```

### Получение баланса проездного

```http
POST /api/v1/travel-card/balance
Content-Type: application/json
```

```json
{
  "phone": "+79846274627",
  "sms_code": "1420"
}
```

Пример ответа:

```json
{
  "ticket_id": 1,
  "phone": "+79846274627",
  "balance": 100,
  "last_entry_station": "Юго-западная"
}
```

## Локальный запуск

```bash
docker compose up --build
```

После запуска:

- Swagger UI: `http://localhost:8000/docs`
- API: `http://localhost:8000`

## Локальные проверки

```bash
python -m pip install -r requirements-dev.txt
python -m ruff check .
python -m bandit -r app
python -m pytest
```

## TeamCity

Файлы Kotlin DSL лежат в каталоге `.teamcity/`.
Перед защитой нужно заменить `StudentIO` в названиях конфигураций на свои фамилию и инициалы, а также заполнить параметры DockerHub и prod-стенда в TeamCity.
