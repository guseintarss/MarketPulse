import json 

async def test_create_user(client,  get_user_from_database):
    user_data = {
        "username":"Vanessa",
        "surname": "Volkovna",
        "email": "fawdawido@mamil.ru",
    }
    resp = client.post("/user/", data=json.dumps(user_data))
    data_from_resp = resp.json()
    assert resp.status_code ==200
    assert data_from_resp["username"] == user_data["username"]
    assert data_from_resp["surname"] == user_data["surname"]
    assert data_from_resp["email"] == user_data["email"]
    users_from_db = await get_user_from_database(data_from_resp["user_id"])
    assert len(users_from_db) == 1
    users_from_db = dict(users_from_db[0])
    assert users_from_db["username"] == user_data["username"]
    assert users_from_db["surname"] == user_data["surname"]
    assert users_from_db["email"] == user_data["email"]
    assert users_from_db["is_active"] is True
    assert str(users_from_db["user_id"]) == data_from_resp["user_id"]   