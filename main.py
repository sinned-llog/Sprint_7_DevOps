from fastapi import FastAPI, HTTPException
from fastapi import Request
from fastapi.responses import JSONResponse
import datetime

api = FastAPI()

data = [1, 2, 3, 4, 5]
@api.get('/data')
def get_data(index):
    try:
        return {
            'data': data[int(index)]
        }
    except IndexError:
        raise HTTPException(
            status_code=404,
            detail='Unknown Index')
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail='Bad Type'
        )

class MyException(Exception):
    def __init__(self,                 
                 name : str,
                 date: str):
        self.name = name
        self.date = date

@api.exception_handler(MyException)
def MyExceptionHandler(
    request: Request,
    exception: MyException
    ):
    return JSONResponse(
        status_code=418,
        content={
            'url': str(request.url),
            'name': exception.name,
            'message': 'This error is my own', 
            'date': exception.date
        }
    )
@api.get('/my_custom_exception')
def get_my_custom_exception():
    raise MyException(
      name='my error',
      date=str(datetime.datetime.now())
      )

responses = {
    200: {"description": "OK"},
    404: {"description": "Item not found"},
    302: {"description": "The item was moved"},
    403: {"description": "Not enough privileges"},
}
@api.get('/thing', responses=responses)
def get_thing():
    return {
        'data': 'hello world'
    }

# from fastapi import FastAPI

# api = FastAPI(
#     title='My API'
# )

# @api.get('/')
# def get_index():
#     return {
#         'data': 'hello world'
#     }

# @api.get('/item/{itemid}')
# def get_item(itemid: str):
#     try:
#         int_id = int(itemid)
#         return {
#             'route': 'dynamic',
#             'itemid': int_id,
#             'source': 'int'
#         }
#     except ValueError:
#         try:
#             float_id = float(itemid)
#             return {
#                 'route': 'dynamic',
#                 'itemid': float_id,
#                 'source': 'float'
#             }
#         except ValueError:
#                 return {
#                 'route': 'dynamic',
#                 'itemid': itemid,
#                 'source': 'string'
#             }

# from fastapi import Header
# @api.get('/headers')
# def get_headers(user_agent=Header(None)):
#     return {
#         'User-Agent': user_agent
#     }

# @api.get('/item/{itemid}/description/{language}')
# def get_item_language(itemid: int, language: str):
#     if language == 'fr':
#         return {
#             'itemid': itemid,
#             'description': 'un objet',
#             'language': 'fr'
#         }
#     else:
#         return {
#             'itemid': itemid,
#             'description': 'an object',
#             'language': 'en'
#         }
    
# @api.get('/')
# def get_index():
#     return {
#         'method': 'get',
#         'endpoint': '/'
#     }

# @api.get('/other')
# def get_other():
#     return {
#         'method': 'get',
#         'endpoint': '/other'
#     }

# @api.post('/')
# def post_index():
#     return {
#         'method': 'post',
#         'endpoint': '/'
#     }

# @api.delete('/')
# def delete_index():
#     return {
#         'method': 'delete',
#         'endpoint': '/'
#     }

# @api.put('/')
# def put_index():
#     return {
#         'method': 'put',
#         'endpoint': '/'
#     }

# @api.patch('/')
# def patch_index():
#     return {
#         'method': 'patch',
#         'endpoint': '/'
#     }