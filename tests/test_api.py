def test_healthcheck(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_index_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "Приложение мастер-классов гончарной мастерской" in response.text


def test_get_workshop_classes(client):
    response = client.get("/api/v1/workshops")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 3
    assert payload[0] == {"id": 1, "name": "Гончарный круг", "price": 3500}
    assert payload[1]["name"] == "Лепим жабу"


def test_get_registration_success(client):
    response = client.post("/api/v1/registrations/info", json={"sms_code": "1871"})

    assert response.status_code == 200
    assert response.json() == {
        "registration_id": 1,
        "sms_code": "1871",
        "workshop_name": "Гончарный круг",
        "registration_time": "18:10",
    }


def test_get_registration_rejects_invalid_code(client):
    response = client.post("/api/v1/registrations/info", json={"sms_code": "9999"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid SMS code"
