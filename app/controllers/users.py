from app.api.crud.users import *

def get_user(param, db):
    user = get_user_by_name(param.name, db)
    if not user:
        return insert_user(param, db)

    return user
