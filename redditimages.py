import requests

def get_hot_posts():

    with open("keys.txt", "r") as f:
        lines = f.read().splitlines()
        CLIENT_ID = lines[0]
        SECRET_TOKEN = lines[1]
    with open("Password", "r") as f:
        pw = f.read()

    # note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_TOKEN)

    # here we pass our login method (password), username, and password
    data = {'grant_type': 'password',
            'username': 'EpicMemesYT',
            'password': pw
            }

    # setup our header info, which gives reddit a brief description of our app
    headers = {'User-Agent': 'MyBot/0.0.1'}

    # send our request for an OAuth token
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)

    # convert response to JSON and pull access_token value

    TOKEN = res.json()['access_token']

    # add authorization to our headers dictionary
    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

    # while the token is valid (~2 hours) we just add headers=headers to our requests
    requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

    res = requests.get("https://oauth.reddit.com/r/cursedimages/hot",
                       headers=headers)

    posts = [post['data']['url'] for post in res.json()['data']['children']]

   # for post in res.json()['data']['children']:

    return posts

print(get_hot_posts())