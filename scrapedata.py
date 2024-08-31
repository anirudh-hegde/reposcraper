import requests
import streamlit as st

github_username = st.text_input("enter the username: ")

# github_username = input("enter your github username: ")
url = f"https://api.github.com/users/{github_username}/repos"

repositories = []
page = 1

while True:

    params = {'page': page}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        repositories.extend(response.json())

        if 'Link' in response.headers:
            links = response.headers['Link'].split(",")
            nextlink = next((link for link in links if 'rel="next"' in link), None)
            if nextlink and 'page' in nextlink:
                page += 1
            else:
                break
        else:
            break
    else:
        print(f"Unable to fetch repositories. Status code:{response.status_code}")
        break
st.success(f"{github_username} GitHub Repositories: \n")
st.success(f"\nTotal public repositories: {len(repositories)}")

for index,repo in enumerate(repositories):
    st.success(f"{index+1}: {repo['name']}")



