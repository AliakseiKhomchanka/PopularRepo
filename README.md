# PopularRepo

[Postman API documentation](https://documenter.getpostman.com/view/17281147/TzzHnYuj)

A simple dockerized Python/Flask-based service for evaluating how popular a certain repository is. Flask has been chosen for its simplicity, since the app itself doesn't require much detail and is pretty much two endpoints with some logic.

Non-default Python libraries used are listed in the [requirements.txt](https://github.com/AliakseiKhomchanka/PopularRepo/blob/main/requirements.txt) file.

## What it does

The service provides two API endpoints, one for health checks and another for fetching data about popularity of any repository. 
Anyone can access the endpoint and get information about repositories that the service has access to (access is defined by the scope of the Github token which is supplied to the service). API documentation is available [here](https://documenter.getpostman.com/view/17281147/TzzHnYuj).

**ASSUMPTION: No authentication or TLS is implemented here under the assumption that a production server of this kind would only be responsible for its own duties while authentication and TLS would be delegated to a reverse proxy in front of the service.**

## How to run it

There are two ways to run the service


### Running the Flask app directly


It is possible to directly run the API server by running the following command:

`python app.py`

After which the API server will be available at `localhost:5000`.

Note that you need to have the POPULAR_REPO_TOKEN environment variable set to the value of the Github token so that the Flask app can read it.

**ASSUMPTION: To simplify the service, the GitHub token is built into it instead of being passed with each request.**


### Running the server via Docker


Another way to run the server is using Docker. First, use the provided [Dockerfile](https://github.com/AliakseiKhomchanka/PopularRepo/blob/main/Dockerfile) to build the image:

`sudo docker build -f Dockerfile .`

After that, assuming that the POPULAR_REPO_TOKEN environment variable has been set to the value of the Github token:

`sudo docker run --network=host -e POPULAR_REPO_TOKEN=$POPULAR_REPO_TOKEN {YOUR_IMAGE_ID}`

After this, the server will be available at `locahhost:5000`.

## How it is documented

API endpoints and example requests are documented via Postman. Published documentation is available [here](https://documenter.getpostman.com/view/17281147/TzzHnYuj).

## How to test it

This repository has a suite of automated API tests executed with Newman. The whole test environment is organized into two Docker services:

- **popular**, which runs the API server
- **newman**, which runs automated tests

Both of those services are deployed together via docker-compose with configuration available [here](https://github.com/AliakseiKhomchanka/PopularRepo/blob/main/docker-compose.yml). Note that the POPULAR_REPO_TOKEN environment variable needs to be set before running docker-compose. After it is set, you can launch the whole thing with:

`sudo -E docker-compose up --build --exit-code-from newman`

## What it doesn't do

As there are time constraints, I haven't implemented everything that would normally be present in a production-ready service. Below are some things that I would improve further.

### Automated CI

It is always more convenient to have tests run automatically on each commit. Setting up something like GitHub Actions for the repository is easy and there are community-made workflow templates for running docker-compose, the only issue would be to resolve a convenient and safe way of storing tokens as we can't just check them into the repo itself.

### Input validation and tests for said validation

Right now it is possible to enter a malformed repo name and simply get a 404 response. While technically true (the repo with a malformed name indeed does not exist), it may confuse users into thinking that the problem is with their credentials (token not having access to the repo), which should be avoided as much as possible.

# Tests for responses 301 and 403 from Github

GitHub API documentation states the it is possible to get 301 Permanently Moved and 403 Forbidden when fetching repositories. However, so far I have been unable to reproduce such behavior and as such it is untested, although the code for handling these cases is there. One solution could be using a mock server that returns predefined responses, but since other tests use actual Github calls (to also check for possible changes in the GitHub API), this would make the whole test suite inconsistent.

