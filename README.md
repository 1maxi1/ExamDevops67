# ExamDevops6 - Билет 22

REST API-приложение для гончарной мастерской. Сервис позволяет получать список
мастер-классов и проверять запись на мастер-класс по SMS-коду.

## Что реализовано

- веб-сервер на FastAPI;
- база данных PostgreSQL;
- начальные данные из билета 22;
- публичный endpoint для получения мастер-классов;
- защищённый endpoint для получения записи по SMS-коду;
- возврат стоимости мастер-классов в публичном списке;
- Dockerfile и `docker-compose.yml`;
- тесты, линтер и SAST-проверка;
- конфигурация TeamCity DSL.

## API

### Проверка работоспособности

```http
GET /health
```

### Список мастер-классов

```http
GET /api/v1/workshops
```

Пример ответа:

```json
[
  {
    "id": 1,
    "name": "Гончарный круг",
    "price": 3500
  }
]
```

### Информация о записи на мастер-класс

```http
POST /api/v1/registrations/info
Content-Type: application/json
```

```json
{
  "sms_code": "1871"
}
```

Пример ответа:

```json
{
  "registration_id": 1,
  "sms_code": "1871",
  "workshop_name": "Гончарный круг",
  "registration_time": "18:10"
}
```

## Локальный запуск

```bash
docker compose up --build
```

После запуска:

- графический интерфейс: `http://localhost:8000/`
- Swagger UI: `http://localhost:8000/docs`

## Локальные проверки

```bash
python -m pip install -r requirements-dev.txt
python -m ruff check .
python -m bandit -r app
python -m pytest
```
