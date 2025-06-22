import os
import requests
import base64
import subprocess
from pathlib import Path


def get_github_file(repo_owner, repo_name, file_path, branch, token=None):
    """
    Get the file under test from ciphers/base32.py repo

    parameters
    repo_owner (str): owner of the repox
    repo_name (str): repo name
    file_path (str): path to the file under test
    token (str, optional): GitHub token
    branch (str, optional): branch name

    return
    str: file content or error info
    """
    # Set header
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"

    # Build url
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    params = {"ref": branch}

    # Get file content
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        if "content" in data:
            content = base64.b64decode(data["content"]).decode("utf-8")
            return content
        else:
            print(f"Error: API returns unexpected format - {data}")
            return None

    # Report error info if failed
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error: {http_err}")
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"Request Error: {req_err}")
        return None
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return None


def clone_github_repo(repo_owner, repo_name, output) -> None:
    """
    Cloning GitHub repo

    parameter
        repo_owner (str): owner of the repox
        repo_name (str): repo name
        output (str): output path
    """
    # Check output path
    Path(output).mkdir(parents=True, exist_ok=True)
    repo_url = f"https://github.com/{repo_owner}/{repo_name}.git"
    output += repo_name

    try:
        # Clone repo
        result = subprocess.run(
            ["git", "clone", repo_url, output],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Clone failed: {e.stderr}")
    except Exception as e:
        print(f"Unexpected error happened when cloning GitHub repo: {str(e)}")
