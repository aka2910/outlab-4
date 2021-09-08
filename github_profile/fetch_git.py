import requests
from requests.exceptions import HTTPError

urls = 'https://api.github.com/users/'


def get_github_users_response(username):
    try:
        response = requests.get(urls + username)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')
        return response.json()


def get_github_repos_response(username):
    try:
        response = requests.get(urls + username + '/repos')
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')
        return response.json()


def filter_json(repo):
    my_str = sorted(repo, key=lambda x: x['stargazers_count'], reverse=True)
    my_js = {"repos": []}
    for item in my_str:
        my_js["repos"].append({"name": item["name"], "stars": item["stargazers_count"]})
    return my_js
