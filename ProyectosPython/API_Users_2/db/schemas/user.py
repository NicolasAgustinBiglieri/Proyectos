def user_schema(user) -> dict:
    return {"id": int(user["id"]),
            "username": user["username"],
            "email": user["email"],
            "firstname": user["firstname"],
            "lastname": user["lastname"],
            "dateofbirth": user["dateofbirth"],
            "country": user["country"],
            "city": user["city"],
            "email_verif": user["email_verif"],
            "registered_date": user["registered_date"]}


def users_schema(users) -> list:
    return [user_schema(user) for user in users]


def user_pass_schema(user) -> dict:
    return {"id": int(user["id"]),
            "username": user["username"],
            "email": user["email"],
            "firstname": user["firstname"],
            "lastname": user["lastname"],
            "dateofbirth": user["dateofbirth"],
            "country": user["country"],
            "city": user["city"],
            "email_verif": user["email_verif"],
            "registered_date": user["registered_date"],
            "password": user["password"]}


