import os
import requests

# definition of the API address
api_address = os.environ.get('API_ADDRESS', 'api')
api_port = os.environ.get('API_PORT', '8000')

# reqest
def send_sentiment_request(api_address, api_port, username, password, version, sentence):
    url=f'http://{api_address}:{api_port}/{version}/sentiment'
    response = requests.get(
        url=url,
        params= {
            'username': username,
            'password': password,
            'sentence': sentence
        }
    )
    return response

def authorization_test(api_address, api_port, username, password, sentence):  
    r_v1 = send_sentiment_request(api_address, api_port, username, password, 'v1', sentence)
    r_v2 = send_sentiment_request(api_address, api_port, username, password, 'v2', sentence)

    output = '''

    =============================
    Authorization test // v1
    =============================
    request done at "/v1/sentiment"
    | username="{username}"
    | password="{password}"
        expected result = 200
    actual result = {status_code_v1}
    ==>  {test_status_v1}
    
    =============================
    Authorization test // v2
    =============================
    request done at "/v2/sentiment"
    | username="{username}"
    | password="{password}"
        expected result = 200
    actual result = {status_code_v2}
    ==>  {test_status_v2}
    '''
    # query status
    status_code_v1 = r_v1.status_code
    status_code_v2 = r_v2.status_code

    # display the results
    test_status_v1 = 'SUCCESS' if status_code_v1 == 200 else 'FAILURE'
    test_status_v2 = 'SUCCESS' if status_code_v2 == 200 else 'FAILURE'

    print(output.format(
        username=username, 
        password=password, 
        status_code_v1=status_code_v1, 
        test_status_v1=test_status_v1,
        status_code_v2=status_code_v2,
        test_status_v2=test_status_v2   
        ))
    
    output_formatted = output.format(
        username=username, 
        password=password, 
        status_code_v1=status_code_v1, 
        test_status_v1=test_status_v1,
        status_code_v2=status_code_v2,
        test_status_v2=test_status_v2   
        )
    return output_formatted

users = [
    {'username': 'alice', 'password': 'wonderland', 'sentence': 'life is beautiful'},
    {'username': 'bob', 'password': 'builder', 'sentence': 'life is beautiful'},
    ]

for user in users:
    result = authorization_test(api_address, api_port, user['username'], user['password'], user['sentence'])
    # printing in a file
    if os.environ.get('LOG') == '1':
        os.makedirs('/logs', exist_ok=True)
        with open('/logs/authorization_test.txt', 'a') as file:
            file.write(result)
