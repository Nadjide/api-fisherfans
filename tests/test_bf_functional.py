import datetime


def create_user(client, **overrides):
    payload = {
        "firstName": "Alice",
        "lastName": "Doe",
        "email": "alice@example.com",
    }
    payload.update(overrides)
    response = client.post("/v1/users/", json=payload)
    assert response.status_code == 201
    return response.json()


def create_boat(client, owner_id, **overrides):
    payload = {
        "name": "Sea Breeze",
        "boatType": "open",
        "ownerId": owner_id,
    }
    payload.update(overrides)
    response = client.post("/v1/boats/", json=payload)
    assert response.status_code == 201
    return response.json()


def create_trip(client, boat_id, **overrides):
    payload = {
        "tripType": "daily",
        "pricingType": "flat",
        "boatId": boat_id,
    }
    payload.update(overrides)
    response = client.post("/v1/trips/", json=payload)
    assert response.status_code == 201
    return response.json()


def create_reservation(client, user_id, trip_id, **overrides):
    payload = {
        "reservedDate": "2026-01-10",
        "seats": 2,
        "userId": user_id,
        "tripId": trip_id,
    }
    payload.update(overrides)
    response = client.post("/v1/reservations/", json=payload)
    assert response.status_code == 201
    return response.json()


def create_logbook(client, author_id, **overrides):
    payload = {
        "title": "Session hiver",
        "authorId": author_id,
    }
    payload.update(overrides)
    response = client.post("/v1/logbooks/", json=payload)
    assert response.status_code == 201
    return response.json()


# BF 2

def test_bf2_resources_exposed(client):
    assert client.get("/v1/users").status_code == 200
    assert client.get("/v1/boats").status_code == 200
    assert client.get("/v1/trips").status_code == 200
    assert client.get("/v1/reservations").status_code == 200
    assert client.get("/v1/logbooks").status_code == 200


# BF 3

def test_bf3_create_user(client):
    user = create_user(client)
    assert user["id"] > 0
    assert user["email"] == "alice@example.com"


# BF 4

def test_bf4_create_boat(client):
    user = create_user(client, email="captain@example.com", boatLicense="LIC-123")
    boat = create_boat(client, user["id"], name="Atlantic")
    assert boat["id"] > 0
    assert boat["ownerId"] == user["id"]


# BF 5

def test_bf5_create_trip(client):
    user = create_user(client, email="owner@example.com", boatLicense="LIC-456")
    boat = create_boat(client, user["id"])
    trip = create_trip(client, boat["id"], title="Sortie matin")
    assert trip["id"] > 0
    assert trip["boatId"] == boat["id"]


# BF 6

def test_bf6_create_reservation(client):
    user = create_user(client, email="angler@example.com", boatLicense="LIC-789")
    boat = create_boat(client, user["id"])
    trip = create_trip(client, boat["id"])
    reservation = create_reservation(client, user["id"], trip["id"])
    assert reservation["id"] > 0
    assert reservation["tripId"] == trip["id"]


# BF 7

def test_bf7_create_logbook(client):
    user = create_user(client, email="logbook@example.com")
    logbook = create_logbook(client, user["id"])
    assert logbook["id"] > 0
    assert logbook["authorId"] == user["id"]


# BF 9

def test_bf9_delete_boat(client):
    user = create_user(client, email="deleteboat@example.com", boatLicense="LIC-999")
    boat = create_boat(client, user["id"])
    response = client.delete(f"/v1/boats/{boat['id']}")
    assert response.status_code == 204
    assert client.get(f"/v1/boats/{boat['id']}").status_code == 404


# BF 14

def test_bf14_update_boat(client):
    user = create_user(client, email="updateboat@example.com", boatLicense="LIC-111")
    boat = create_boat(client, user["id"], name="Old Name")
    response = client.put(
        f"/v1/boats/{boat['id']}",
        json={"name": "New Name"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"


# BF 21

def test_bf21_filter_boats_by_user(client):
    user1 = create_user(client, email="owner1@example.com", boatLicense="LIC-201")
    user2 = create_user(client, email="owner2@example.com", boatLicense="LIC-202")
    boat1 = create_boat(client, user1["id"], name="Boat One")
    create_boat(client, user2["id"], name="Boat Two")

    response = client.get(f"/v1/boats?userId={user1['id']}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == boat1["id"]


# BF 24

def test_bf24_filter_boats_by_bounding_box(client):
    user = create_user(client, email="bbox@example.com", boatLicense="LIC-303")
    create_boat(client, user["id"], name="Near", latitude=43.6, longitude=1.43)
    create_boat(client, user["id"], name="Far", latitude=48.85, longitude=2.35)

    response = client.get(
        "/v1/boats?minLat=43.0&maxLat=44.0&minLng=1.0&maxLng=2.0"
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Near"


# BF 25

def test_bf25_business_error_codes(client):
    create_user(client, email="dup@example.com")
    response = client.post(
        "/v1/users/",
        json={"firstName": "Dup", "lastName": "User", "email": "dup@example.com"},
    )
    assert response.status_code == 409

    response = client.get("/v1/boats/9999")
    assert response.status_code == 404


# BF 26

def test_bf26_prevent_trip_creation_without_boat(client):
    response = client.post(
        "/v1/trips/",
        json={"tripType": "daily", "pricingType": "flat", "boatId": 9999},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Boat not found"


# BF 27

def test_bf27_prevent_boat_creation_without_license(client):
    user = create_user(client, email="nolicense@example.com")
    response = client.post(
        "/v1/boats/",
        json={
            "name": "No License",
            "boatType": "open",
            "ownerId": user["id"],
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Boat license required"
