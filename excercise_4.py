from pydantic import BaseModel
from typing import Optional, List
from fastapi import FastAPI

class User(BaseModel):
    user_id: Optional[int] = None
    name: str
    subscription: str

api = FastAPI()

users_db = [
    {
        'user_id': 1,
        'name': 'Alice',
        'subscription': 'free tier'
    },
    {
        'user_id': 2,
        'name': 'Bob',
        'subscription': 'premium tier'
    },
    {
        'user_id': 3,
        'name': 'Clementine',
        'subscription': 'free tier'
    }
]
@api.post('/users')
def post_user(user: User):
    new_id = max([u['user_id'] for u in users_db]) + 1 if users_db else 1
    new_user = {
        'user_id': new_id,
        'name': user.name,
        'subscription': user.subscription
    }
    users_db.append(new_user)
    return new_user

@api.put('/users/{userid}')
def put_user(userid: int, user: User):
    for u in users_db:
        if u['user_id'] == userid:
            u['name'] = user.name
            u['subscription'] = user.subscription
            return u
    return {'error': 'User not found'}

@api.delete('/users/{userid}')
def delete_user(userid: int):
    for i, u in enumerate(users_db):
        if u['user_id'] == userid:
            deleted_user = users_db.pop(i)
            return {
                "user_id": deleted_user['user_id'],
                "name": deleted_user['name'],
                "message": 'User deleted successfully'
            }
    return {'error': 'User not found'}




# @api.get('/')
# def get_index(argument1):
#     return {
#         'data': argument1
#     }

# @api.get('/typed')
# def get_typed(argument1: int):
#     return {
#         'data': argument1 + 1
#     }

# @api.get('/addition')
# def get_addition(a: int, b: Optional[int] = None):
#     print(f"a: {a}, b: {b}")
#     if b is not None:
#         result = a + b
#     else:
#         result = a + 1
#     return {
#         'addition_result': result
#     }

# api = FastAPI(
#     title='My API'
# )

# users_db = [
#     {key=lambda x: x['user_id'])['user_id'] + 1 if users_db else 1
#         'user_id': 1,
#         'name': 'Alice',
#         'subscription': 'free tier'
#     },
#     {
#         'user_id': 2,
#         'name': 'Bob',
#         'subscription': 'premium tier'
#     },
#     {
#         'user_id': 3,
#         'name': 'Clementine',
#         'subscription': 'free tier'
#     }
# ]

# @api.get('/')
# def get_index():
#     return {
#         'welcome_message': 'welcome'
#     }

# @api.get('/users')
# def get_users():
#     return users_db

# @api.get('/users/{userid}')
# def get_user_id(userid: int):
#     user = next((x for x in users_db if x.get('user_id') == userid), {})
#     return user

# @api.get('/users/{userid}/name')
# def get_user_name(userid: int):
#     user_name = next((x.get('name') for x in users_db if x.get('user_id') == userid), None)
#     return {'name': user_name} if user_name else {}

# @api.get('/users/{userid}/subscription')
# def get_user_subscription(userid: int):
#     user_subscription = next((x.get('subscription') for x in users_db if x.get('user_id') == userid), None)
#     return {'subscription': user_subscription} if user_subscription else {}