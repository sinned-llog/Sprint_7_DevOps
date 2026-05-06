import os
import requests

# definition of the API address
api_address = "127.0.0.1"
api_port = 8000
username = 'alice'
password = 'wonderland'
sentence = 'life is beautiful'
# reqest    
r_v1 = requests.get(
    'http://{address}:{port}/v1/sentiment'.format(address=api_address, port=api_port),
    params= {
        'username': 'alice',
        'password': 'wonderland'
        
    }
)
output = '''

=============================
Authentication test
=============================
request done at "/v1/sentiment"
    | username="{username}"
    | password="{password}"
    expected result = 200
    actual result = {status_code}
    ==>  {test_status}
    '''
    # query status
status_code = r_v1.status_code

# display the results
if status_code == 200:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'

print(output.format(
    username=username, 
    password=password, 
    status_code=status_code, 
    test_status=test_status
    ))

users = [
    {'username': 'alice', 'password': 'wonderland'},
    {'username': 'bob', 'password': 'builder'},
    {'username': 'clementine', 'password': 'mandarin'},
    ]

