import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000/v1"

def seed_db():
    print("🚀 Starting Massive Seeding...")
    session = requests.Session()

    # --- 1. USERS ---
    users_to_create = [
        {
            "firstName": "Nawfel", "lastName": "Fisher", "email": "nawfel@fisherfans.com", "password": "password123",
            "phone": "0600000001", "address": "123 Rue de la Mer", "postalCode": "06000", "city": "Nice",
            "status": "professional", "activityType": "guide", "company": "FisherFans Inc", "siret": "12345678901234",
            "languages": ["French", "English"]
        },
        {
            "firstName": "Alice", "lastName": "Ocean", "email": "alice@ocean.com", "password": "password123",
            "phone": "0600000002", "address": "45 Boulevard des Vagues", "postalCode": "06300", "city": "Nice",
            "status": "individual", "languages": ["French", "Italian"], "avatarUrl": "https://example.com/alice.jpg"
        },
        {
            "firstName": "Bob", "lastName": "Boat", "email": "bob@boats.com", "password": "password123",
            "phone": "0600000003", "city": "Cannes", "status": "individual", "boatLicense": "LIC-987-XYZ"
        },
        {
            "firstName": "Charlie", "lastName": "Tuna", "email": "charlie@tuna.com", "password": "password123",
            "phone": "0600000004", "city": "Monaco", "status": "individual", "insuranceNumber": "INS-111-222"
        }
    ]

    tokens = {}
    for user_data in users_to_create:
        print(f"👤 User: {user_data['email']}")
        session.post(f"{BASE_URL}/auth/register", json=user_data)
        r = session.post(f"{BASE_URL}/auth/token", data={"username": user_data["email"], "password": user_data["password"]})
        if r.status_code == 200:
            tokens[user_data["email"]] = r.json()["access_token"]

    if not tokens: return

    nawfel_h = {"Authorization": f"Bearer {tokens['nawfel@fisherfans.com']}"}
    alice_h = {"Authorization": f"Bearer {tokens['alice@ocean.com']}"}
    bob_h = {"Authorization": f"Bearer {tokens['bob@boats.com']}"}
    charlie_h = {"Authorization": f"Bearer {tokens['charlie@tuna.com']}"}

    # --- 2. BOATS ---
    boats = [
        {
            "name": "Marlin King", "description": "Perfect for deep sea.", "brand": "Boston Whaler",
            "yearBuilt": 2023, "boatType": "cabin", "propulsion": "gasoline", "enginePowerHP": 600,
            "homePort": "Nice Port", "maxCapacity": 10, "berths": 2, "depositEUR": 2500.0, "ownerId": 1,
            "requiredLicense": "coastal", "equipment": ["GPS", "Sonar", "Fishing rods"], "latitude": 43.696, "longitude": 7.285
        },
        {
            "name": "Quick Strike", "description": "Fast and agile.", "brand": "Zodiac",
            "yearBuilt": 2021, "boatType": "open", "propulsion": "gasoline", "enginePowerHP": 150,
            "homePort": "Antibes", "maxCapacity": 6, "ownerId": 1, "equipment": ["Life jackets"]
        },
        {
            "name": "Silenzio", "description": "Quiet sailboat.", "brand": "Beneteau",
            "yearBuilt": 2018, "boatType": "sailboat", "propulsion": "diesel", "enginePowerHP": 50,
            "homePort": "Cannes", "maxCapacity": 8, "berths": 4, "ownerId": 3, "latitude": 43.551, "longitude": 7.016
        }
    ]
    boat_ids = []
    for b in boats:
        print(f"🚤 Boat: {b['name']}")
        h = nawfel_h if b["ownerId"] == 1 else bob_h
        r = session.post(f"{BASE_URL}/boats/", json=b, headers=h)
        if r.status_code == 201: boat_ids.append(r.json()["id"])

    # --- 3. TRIPS ---
    trips = [
        {
            "title": "Tuna Hunting", "description": "Catch massive bluefin.", "tripType": "daily", "pricingType": "per_person",
            "startDates": ["2026-07-01"], "endDates": ["2026-07-01"], "startTimes": ["06:00:00"], "endTimes": ["18:00:00"],
            "passengerCount": 6, "price": 150.0, "boatId": 1
        },
        {
            "title": "Sunset Cruise & Fish", "description": "Relax and fish.", "tripType": "daily", "pricingType": "flat",
            "startDates": ["2026-07-05"], "endDates": ["2026-07-05"], "startTimes": ["18:00:00"], "endTimes": ["22:00:00"],
            "passengerCount": 4, "price": 300.0, "boatId": 2
        },
        {
            "title": "Sail & Jig", "description": "Sailing and jigging.", "tripType": "recurring", "pricingType": "per_person",
            "startDates": ["2026-08-01", "2026-08-08"], "endDates": ["2026-08-01", "2026-08-08"], "startTimes": ["09:00:00"], "endTimes": ["15:00:00"],
            "passengerCount": 6, "price": 100.0, "boatId": 3
        }
    ]
    trip_ids = []
    for t in trips:
        print(f"🎣 Trip: {t['title']}")
        h = nawfel_h if t["boatId"] in [1, 2] else bob_h
        r = session.post(f"{BASE_URL}/trips/", json=t, headers=h)
        if r.status_code == 201: trip_ids.append(r.json()["id"])

    # --- 4. RESERVATIONS ---
    if len(trip_ids) >= 2:
        res = [
            {"reservedDate": "2026-07-01", "seats": 2, "totalPrice": 300.0, "userId": 2, "tripId": trip_ids[0]},
            {"reservedDate": "2026-07-01", "seats": 1, "totalPrice": 150.0, "userId": 4, "tripId": trip_ids[0]},
            {"reservedDate": "2026-07-05", "seats": 4, "totalPrice": 300.0, "userId": 3, "tripId": trip_ids[1]}
        ]
        for r_data in res:
            print(f"📅 Reservation: User {r_data['userId']} -> Trip {r_data['tripId']}")
            h = {2: alice_h, 3: bob_h, 4: charlie_h}[r_data["userId"]]
            session.post(f"{BASE_URL}/reservations/", json=r_data, headers=h)

    # --- 5. LOGBOOKS ---
    logbooks = [
        {"title": "My Nice Catches", "authorId": 1},
        {"title": "Ocean Diary", "authorId": 2},
        {"title": "Sailor's Fish", "authorId": 3}
    ]
    for lb in logbooks:
        print(f"📖 Logbook: {lb['title']}")
        h = {1: nawfel_h, 2: alice_h, 3: bob_h}[lb["authorId"]]
        r = session.post(f"{BASE_URL}/logbooks/", json=lb, headers=h)
        if r.status_code == 201:
            l_id = r.json()["id"]
            pages = [
                {"fishName": "Sea Bass", "comment": "Good size.", "lengthCm": 55, "weightKg": 3.2, "fishingLocation": "Nice", "fishingDate": "2025-01-10", "released": True, "logbookId": l_id},
                {"fishName": "Dorade", "comment": "Tasty.", "lengthCm": 40, "weightKg": 1.5, "fishingLocation": "Cannes", "fishingDate": "2025-01-15", "released": False, "logbookId": l_id}
            ]
            for p in pages:
                session.post(f"{BASE_URL}/logbooks/{l_id}/pages", json=p, headers=h)

    print("✅ Massive Seeding completed!")

if __name__ == "__main__":
    seed_db()
