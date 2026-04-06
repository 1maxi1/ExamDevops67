def test_healthcheck(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_index_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "Приложение проездного билета" in response.text


def test_get_metro_changes(client):
    response = client.get("/api/v1/metro/changes")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 3
    assert payload[0]["description"] == "Закрытие станции Рижская"
    assert payload[1]["affected_line"] == "Кольцевая"


def test_get_balance_success(client):
    response = client.post(
        "/api/v1/travel-card/balance",
        json={"phone": "+79846274627", "sms_code": "1420"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "ticket_id": 1,
        "phone": "+79846274627",
        "balance": 100,
        "last_entry_station": "Юго-западная",
    }


def test_get_balance_rejects_invalid_credentials(client):
    response = client.post(
        "/api/v1/travel-card/balance",
        json={"phone": "+79846274627", "sms_code": "9999"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid phone number or SMS code"
