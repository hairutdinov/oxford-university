from uuid import uuid4

from tests.conftest import create_test_auth_headers_for_user


async def test_delete_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Nikolai",
        "surname": "Sviridov",
        "email": "lol@kek.com",
        "is_active": True,
        "hashed_password": "SampleHashedPass",
    }
    await create_user_in_database(**user_data)
    resp = await client.delete(
        "/user/",
        headers=create_test_auth_headers_for_user(user_data["email"]),
    )
    assert resp.status_code == 200
    assert resp.json() == {"deleted_user_id": str(user_data["user_id"])}
    user_from_db = await get_user_from_database(user_data["user_id"])
    assert user_from_db.name == user_data["name"]
    assert user_from_db.surname == user_data["surname"]
    assert user_from_db.email == user_data["email"]
    assert user_from_db.is_active is False
    assert user_from_db.user_id == user_data["user_id"]


async def test_delete_user_invalid_credentials(client, create_user_in_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Nikolai",
        "surname": "Sviridov",
        "email": "lol@kek.com",
        "is_active": True,
        "hashed_password": "SampleHashedPass",
    }
    await create_user_in_database(**user_data)
    resp = await client.delete(
        "/user/",
        headers=create_test_auth_headers_for_user("wrong@email.com"),
    )
    assert resp.status_code == 401
    assert resp.json() == {"detail": "Could not validate credentials"}
    assert resp.headers["www-authenticate"] == "Bearer"


async def test_delete_user_while_user_not_active(client, create_user_in_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Nikolai",
        "surname": "Sviridov",
        "email": "lol@kek.com",
        "is_active": False,
        "hashed_password": "SampleHashedPass",
    }
    await create_user_in_database(**user_data)
    resp = await client.delete(
        "/user/",
        headers=create_test_auth_headers_for_user(user_data["email"]),
    )
    assert resp.status_code == 400
    data_from_response = resp.json()
    assert data_from_response == {"detail": "Inactive user"}


async def test_delete_user_no_jwt(client, create_user_in_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Nikolai",
        "surname": "Sviridov",
        "email": "lol@kek.com",
        "is_active": True,
        "hashed_password": "SampleHashedPass",
    }
    await create_user_in_database(**user_data)
    resp = await client.delete(
        "/user/",
    )
    assert resp.status_code == 401
    assert resp.json() == {"detail": "Not authenticated"}
