import pytest

from app import app, calculate_calories


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200

    data = response.get_json()
    assert data["application"] == "ACEest Fitness & Gym"
    assert data["status"] == "running"


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "UP"}


def test_programs(client):
    response = client.get("/programs")
    assert response.status_code == 200

    data = response.get_json()
    names = [program["name"] for program in data["programs"]]

    assert "Fat Loss" in names
    assert "Muscle Gain" in names
    assert "Beginner" in names


def test_get_existing_program(client):
    response = client.get("/programs/Fat%20Loss")

    assert response.status_code == 200
    data = response.get_json()

    assert data["name"] == "Fat Loss"
    assert data["factor"] == 22


def test_get_missing_program(client):
    response = client.get("/programs/Unknown")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Program not found"


def test_calculate_calories_function():
    assert calculate_calories(70, "Fat Loss") == 1540
    assert calculate_calories(70, "Muscle Gain") == 2450
    assert calculate_calories(70, "Beginner") == 1820


def test_calculate_calories_api(client):
    response = client.post(
        "/calculate-calories",
        json={"weight": 70, "program": "Fat Loss"},
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "weight": 70.0,
        "program": "Fat Loss",
        "calories": 1540,
    }


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"weight": 70},
        {"program": "Fat Loss"},
    ],
)
def test_calculate_calories_missing_fields(client, payload):
    response = client.post("/calculate-calories", json=payload)

    assert response.status_code == 400


def test_calculate_calories_invalid_program(client):
    response = client.post(
        "/calculate-calories",
        json={"weight": 70, "program": "Unknown"},
    )

    assert response.status_code == 400


def test_calculate_calories_invalid_weight(client):
    response = client.post(
        "/calculate-calories",
        json={"weight": 0, "program": "Fat Loss"},
    )

    assert response.status_code == 400


def test_create_client(client):
    response = client.post(
        "/clients",
        json={
            "name": "Test Client",
            "age": 26,
            "weight": 70,
            "program": "Fat Loss",
        },
    )

    assert response.status_code == 201
    data = response.get_json()

    assert data["message"] == "Client profile validated"
    assert data["client"]["name"] == "Test Client"
    assert data["client"]["estimated_calories"] == 1540


def test_create_client_missing_fields(client):
    response = client.post(
        "/clients",
        json={"name": "Test Client", "age": 26},
    )

    assert response.status_code == 400
    assert "fields" in response.get_json()


def test_create_client_invalid_program(client):
    response = client.post(
        "/clients",
        json={
            "name": "Test Client",
            "age": 26,
            "weight": 70,
            "program": "Unknown",
        },
    )

    assert response.status_code == 400
