import requests
from dotenv import load_dotenv
from datetime import datetime
import os
load_dotenv()
import json

headers = {"accept": "application/vnd.github.v3+json",
           "Authorization": f"token {os.getenv('TOKEN')}"
          }

def get_data(repository_name,information_type):
    if information_type == "pull-requests":
        command = "pulls"
    elif information_type == "issues":
        command = 'issues'
    res = requests.get(f"https://api.github.com/repos/{repository_name}/{command}",headers=headers)
    return res

def print_data(data,information_type):
    if information_type == "pull-requests":
        fmt = "PR-"
    elif information_type == "issues":
        fmt = "#"
    for pr in data:
        print(f"{fmt}{pr['number']} -- {pr['title']}")
        print(f"Created by {pr['user']['login']} on {datetime.strptime(pr['created_at'], '%Y-%m-%dT%H:%M:%SZ').strftime('%B %d , %Y')}")
        print(f"PR is {pr['state']}\n")

repository_name = input(
    "Enter the repository name (format: owner/repository) :")

information_type = input(
    "Enter the information type (pull-requests, issues) :")

data = get_data(repository_name,information_type)
if data.status_code != 200 :
    print("ERROR")
    quit()
data = json.loads(data.text)
data = data[:10]
print(f"Repository {repository_name} top 10 {information_type} are :\n")
print_data(data,information_type)