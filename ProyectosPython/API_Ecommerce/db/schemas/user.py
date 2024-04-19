def user_schema(user) -> dict:
    return {"id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"],
            "firstname": user["firstname"],
            "lastname": user["lastname"],
            "dateofbirth": user["dateofbirth"],
            "country": user["country"],
            "city": user["city"],
            "email_verif": user["email_verif"]}


def users_schema(users) -> list:
    return [user_schema(user) for user in users]


def user_pass_schema(user) -> dict:
    return {"id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"],
            "firstname": user["firstname"],
            "lastname": user["lastname"],
            "dateofbirth": user["dateofbirth"],
            "country": user["country"],
            "city": user["city"],
            "email_verif": user["email_verif"],
            "password": user["password"]}


