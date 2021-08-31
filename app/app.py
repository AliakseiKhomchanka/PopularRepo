from flask import Flask, make_response
from repos import RepoProcessor


app = Flask(__name__)
processor = RepoProcessor()


@app.route("/service/live", methods=["GET"])
def liveness_probe():
    """
    An endpoint for the liveness probe
    :return:
    """
    return "I am still alive!"


@app.route("/repos/popularity/<path:repo>", methods=["GET"])
def repo_popularity(repo):
    """
    Return data about popularity of the particular repo
    :return: response to the client request
    """
    data, code, headers = processor.get_repo_popularity(repo)
    response = make_response(data, code)
    for header in headers.keys():
        response.headers[header] = headers[header]
    return response

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
    