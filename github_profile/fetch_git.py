import requests

urls = 'https://api.github.com/users/'


def get_github_users_response(username):
    try:
        response = requests.get(urls + username)
        response.raise_for_status()
    except Exception as err:
        print(f'error occurred: {err}')
    else:
        return response.json()


def get_github_repos_response(username):
    try:
        response = requests.get(urls + f'{username}/repos')
        response.raise_for_status()
    except Exception as err:
        print(f'error occurred: {err}')
    else:
        return response.json()


def filter_json(repo):
    my_rep = sorted(repo, key=lambda x: x['stargazers_count'], reverse=True)
    my_js = {"repos": []}
    for item in my_rep:
        my_js["repos"].append({"name": item["name"], "stars": item["stargazers_count"]})
    return my_js
