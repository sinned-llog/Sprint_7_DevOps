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

def extract_score(response):
    try:
        return response.json().get('score', None)
    except Exception as e:
        print(f"Error extracting score: {e}")
        return None 

def evaluate_sentiment(api_address, api_port, username, password, sentence):  
    r_v1 = send_sentiment_request(api_address, api_port, username, password, 'v1', sentence)
    r_v2 = send_sentiment_request(api_address, api_port, username, password, 'v2', sentence)

    output = '''

    =============================
    content test // v1
    =============================
    request done at "/v1/sentiment"
    | username="{username}"
    | password="{password}"
    | sentence="{sentence}" 
        score = {score_v1}
        sentiment = {sentiment_v1}
    
    =============================
    content test // v2
    =============================
    request done at "/v2/sentiment"
    | username="{username}"
    | password="{password}"
    | sentence="{sentence}"
        score = {score_v2}
        sentiment = {sentiment_v2}
    '''
    # check the sentiment of the scores
    score_v1 = extract_score(r_v1)
    score_v2 = extract_score(r_v2)
    sentiment_v1 = 'positive' if score_v1 is not None and score_v1 >= 0 else 'negative' if score_v1 is not None and score_v1 < 0 else 'neutral'
    sentiment_v2 = 'positive' if score_v2 is not None and score_v2 >= 0 else 'negative' if score_v2 is not None and score_v2 < 0 else 'neutral'

    # display the results
    print(output.format(
        username=username, 
        password=password, 
        sentence=sentence,
        score_v1=score_v1,
        sentiment_v1=sentiment_v1,
        score_v2=score_v2,
        sentiment_v2=sentiment_v2
    ))
    
    output_formatted = output.format(
        username=username, 
        password=password, 
        score_v1=score_v1,
        sentiment_v1=sentiment_v1,
        score_v2=score_v2,
        sentiment_v2=sentiment_v2,
        sentence=sentence,
    )
    return output_formatted 

# users to test, senteces to test
users = [
    {'username': 'alice', 'password': 'wonderland'},
    ]

sentences = [
    'life is beautiful',
    'that sucks'
]

for user in users:
    for sentence in sentences:
        result = evaluate_sentiment(api_address, api_port, user['username'], user['password'], sentence)
        # printing in a file
        if os.environ.get('LOG') == '1':
            os.makedirs('/logs', exist_ok=True)
            with open('/logs/content_test.txt', 'a') as file:
                file.write(result)
