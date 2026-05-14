# Mid Term Exam - Status Dashboard

Internal Status Dashboard service for Acme Internal Tools Ltd.

## Architecture
* **App:** Python Flask (Dependencies pinned via Poetry)
* **Container:** Docker (Runs as non-root on 127.0.0.1:5000)
* **Proxy:** Nginx (Host-level reverse proxy on port 80)

## How I Solved the Exam Steps
Here is a short summary of how I built each part of the project:

1. **Flask App:** I created `app.py` with the required endpoints. It checks for the `API_KEY` when starting and crashes if it's missing. The `/api/status` endpoint uses a smart 302 redirect with a JSON body so standard curl works easily.
2. **Docker:** I used `python:3.12-slim` as the base image. I created an `appuser` so the app runs safely as a non-root user. I used Poetry to install the pinned dependencies. 
3. **Nginx:** I set up a reverse proxy listening on port 80 that sends traffic to `127.0.0.1:5000`. I added a rewrite rule for the secret endpoint and included all the required proxy headers.
4. **Install Script:** I wrote a bash script that checks for root permissions and the API key. It is idempotent - it stops and removes the old container before building and starting the new one. It also enables and reloads Nginx automatically.
5. **Git Workflow:** I followed the rules and worked with 5 different feature branches. I created a Pull Request for each step and merged them into `main` one by one with clear descriptions.

## What You Need (Prerequisites)
To run this project on a new machine, you must have:
* Linux
* Docker
* Nginx
* Git

## Settings (Environment Variables)
The application uses these variables:
* `API_KEY` - **Required.** The secret key to access the API. The app will not start without it.
* `PORT` - Optional. The port for the Flask app. Default is 5000.
* `VERSION` - Optional. The app version. Default is "1.0.0".

## Run Instructions

To deploy the service on a fresh Ubuntu VM, clone the repo and run the setup script. 
**Note:** The `API_KEY` environment variable is required.

```bash
git clone https://github.com/GalHillel/Mid-Term-Exam.git
cd Mid-Term-Exam
sudo API_KEY=letmein ./install.sh
```

## How to Test
You can verify the deployment using the following commands:

```bash
# Check basic status
curl -s http://localhost/api/status | jq .

# Check secret endpoint without key (should return 401 error)
curl -s -o /dev/null -w "%{http_code}\n" http://localhost/api/secret

# Check secret endpoint with key (should return success message)
curl -s -H "X-API-Key: letmein" http://localhost/api/secret | jq .
```

## How to Fix Problems (Debug)
If the app is not working, check these:

* Check if the container is running: `docker ps`
* Read app errors: `docker logs status-dashboard`
* Check Nginx status: `systemctl status nginx`

## Manual Run (For Developers)
If you want to run the app locally without Docker:

```bash
export API_KEY=letmein
poetry install
poetry run python app.py
```