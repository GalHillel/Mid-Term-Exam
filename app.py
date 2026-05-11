import os
import sys
import socket
from flask import Flask, jsonify, redirect, request

app = Flask(__name__)

PORT = int(os.environ.get("PORT", 5000))
VERSION = os.environ.get("VERSION", "1.0.0")
API_KEY = os.environ.get("API_KEY")

if not API_KEY:
    print("FATAL ERROR: API_KEY environment variable is not set.")
    sys.exit(1)

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Status Dashboard</title>
        <style>body { font-family: sans-serif; padding: 20px; }</style>
    </head>
    <body>
        <h1>Status Dashboard</h1>
        <p>Welcome to the Acme Internal Tools status service.</p>
        <button onclick="fetchStatus()">Check Status</button>
        <pre id="result" style="margin-top: 20px; background: #f4f4f4; padding: 10px; border-radius: 5px; display: none;"></pre>
        
        <script>
        function fetchStatus() {
            fetch('/api/v1/status')
                .then(response => response.json())
                .then(data => {
                    const resultDiv = document.getElementById('result');
                    resultDiv.style.display = 'block';
                    resultDiv.innerText = JSON.stringify(data, null, 2);
                })
                .catch(error => console.error('Error:', error));
        }
        </script>
    </body>
    </html>
    """

@app.route('/api/status')
def status_redirect():
    return redirect('/api/v1/status', code=302)

@app.route('/api/v1/status')
def status_v1():
    return jsonify({
        "status": "ok",
        "hostname": socket.gethostname(),
        "version": VERSION
    })

@app.route('/api/v1/secret')
def secret():
    request_api_key = request.headers.get('X-API-Key')
    if request_api_key == API_KEY:
        return jsonify({"message": "you found the secret"})
    return "Unauthorized\n", 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)