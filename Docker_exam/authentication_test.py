import os
import requests

# definition of the API address
api_address = '127.0.0.1'
# API port
api_port = 8000

# reqest
def authentication_test(api_address, api_port, username, password):
    url=f'http://{api_address}:{api_port}/permissions'
    r = requests.get(
        url=url,
        params= {
            'username': username,
            'password': password
        }
    )
    output = '''

    =============================
    Authentication test
    =============================
    request done at "/permissions"
    | username="{username}"
    | password="{password}"
        expected result = 200
    actual result = {status_code}
    ==>  {test_status}
    '''
    # query status
    status_code = r.status_code

    # display the results
    if status_code == 200:
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'

    print(output.format(username=username, password=password, status_code=status_code, test_status=test_status))
    return output

users = [
    {'username': 'alice', 'password': 'wonderland'},
    {'username': 'bob', 'password': 'builder'},
    {'username': 'clementine', 'password': 'mandarin'},
    ]

for user in users:
    result = authentication_test(api_address, api_port, user['username'], user['password'])
    # printing in a file
    if os.environ.get('LOG') == '1':
        with open('api_test.log', 'a') as file:
            file.write(result)


