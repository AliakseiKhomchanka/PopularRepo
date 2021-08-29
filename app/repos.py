import requests
import os


GH_API_ENDPOINT = os.environ.get("GH_API_ENDPOINT", "https://api.github.com")
POPULAR_REPO_TOKEN = os.environ.get("POPULAR_REPO_TOKEN", "")


class RepoProcessor:

    def __init__(self, pop_threshold=500):
        self.token = POPULAR_REPO_TOKEN
        self.pop_threshold = pop_threshold

    def get_repository(self, repo: str):
        """
        Get information about a particular repository (does a request to GitHubAPI)
        :param repo: repository name in the OWNER/REPO format
        :return: responses status code and payload from GitHub API containing information about the repo in JSON format
        """

        url = GH_API_ENDPOINT + "/repos/" + repo
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": "Bearer {token}".format(token=self.token)
        }
        response = requests.get(url=url, headers=headers)
        return response.status_code, response.headers, response.json()

    def get_repo_popularity(self, repo: str) -> tuple:
        """
        Calculate the popularity score of a given repository
        :param repo: repository name in the OWNER/REPO format OR the full URL
        :return: a dictionary with information about repo's popularity
        """
        response_code, headers, repo_info = self.get_repository(repo)
        # If a repo does not exist (or token doesn't have enough access to see it)
        if response_code == 404:
            return ({
                "repo": repo,
                "status": "not found"
            }, 404, {})
        # If a repo is forbidden
        if response_code == 403:
            return ({
                "repo": repo,
                "status": "forbidden"
            }, 403, {})
        # If a repo endpoint has been moved
        if response_code == 301:
            return ({
                "repo": repo,
                "status": "moved permanently"
            }, 301, {"Location": headers["Location"]})
        # Normal case, repo exists
        score = repo_info["stargazers_count"] + repo_info["forks_count"]*2
        return ({
            "repo": repo,
            "status": "found",
            "score": score,
            "popular": (True if score > 500 else False)
        }, 200, {})
