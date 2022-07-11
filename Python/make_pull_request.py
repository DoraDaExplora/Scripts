import sys
import argparse
import os
import json
import requests

auth_key = f'token {os.environ.get("NPM_TOKEN")}'

parser = argparse.ArgumentParser()
parser.add_argument('head', help='Specify the head branch name')
parser.add_argument('base', help='Specify the branch you want to merge into')
parser.add_argument('owner', help='Specify the repository owner')
parser.add_argument('repo', help='Specify the repository name')
parser.add_argument(
    '--pull_title', help='Specify the pull request title, optional.', const='', nargs='?')

args = parser.parse_args()

api_url = f'https://api.github.com/repos/{args.owner}/{args.repo}/pulls'

req_headers = {
    'accept': 'application/vnd.github+json',
    'Authorization': auth_key
}

data = {
    'owner': args.owner,
    'repo': args.repo,
    'title': args.pull_title,
    'body': '',
    'head': args.head,
    'base': args.base,
}

payload = json.dumps(data)

if auth_key == None:
    sys.exit('No GitHub auth key was found.')

req = requests.post(url=api_url, headers=req_headers, data=payload)

print(f'Got a response: {req.status_code}')

if req.status_code == 201:
    res = req.json()
    print(f'Pull request URL: {res.get("html_url")}')
    sys.exit()
else:
    sys.exit('Operation did not complete.')