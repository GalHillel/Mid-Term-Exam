# Mid Term Exam


Internal Status Dashboard service for Acme Internal Tools Ltd.

## Architecture
* **App:** Python Flask (Dependencies pinned via Poetry)
* **Container:** Docker (Runs as non-root on 127.0.0.1:5000)
* **Proxy:** Nginx (Host-level reverse proxy on port 80)

## Run Instructions

To deploy the service on a fresh Ubuntu VM, clone the repo and run the setup script. 
**Note:** You must provide an `API_KEY` environment variable for the app to start. 

**Note:** The API_KEY environment variable is strictly required.

```bash
git clone https://github.com/GalHillel/Mid-Term-Exam.git
cd Mid-Term-Exam
sudo API_KEY=letmein ./install.sh
```

## Verification

You can verify the deployment using the following commands:

```bash
# Check basic status
curl -s http://localhost/api/status | jq .

# Check secret endpoint without key (should return 401)
curl -s -o /dev/null -w "%{http_code}\n" http://localhost/api/secret

# Check secret endpoint with key
curl -s -H "X-API-Key: letmein" http://localhost/api/secret | jq .
```