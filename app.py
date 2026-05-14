import os
import sys
import socket
import json
from flask import Flask, jsonify, request, Response

app = Flask(__name__)

PORT = int(os.environ.get("PORT", 5000))
VERSION = os.environ.get("VERSION", "1.0.0")
API_KEY = os.environ.get("API_KEY")

if not API_KEY:
    print("FATAL ERROR: API_KEY environment variable is not set.")
    sys.exit(1)


@app.route('/')
def index():
    """Returns the static HTML dashboard page."""
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
        <pre id="res" style="margin-top:20px; background:#f4f4f4; padding:10px; display:none;"></pre>
        
        <script>
        function fetchStatus() {
            fetch('/api/v1/status')
                .then(r => r.json())
                .then(d => {
                    const el = document.getElementById('res');
                    el.style.display = 'block';
                    el.innerText = JSON.stringify(d, null, 2);
                });
        }
        </script>
    </body>
    </html>
    """

@app.route('/api/status')
def status_redirect():
    """Redirects to v1 while providing JSON body for non-L curls."""
    data = {
        "status": "ok",
        "hostname": socket.gethostname(),
        "version": VERSION,
    }
    response = Response(
        response=json.dumps(data),
        status=302,
        mimetype='application/json'
    )
    response.headers['Location'] = '/api/v1/status'
    return response

@app.route('/api/v1/status')
def status_v1():
    """Returns the current status in JSON format."""
    return jsonify({
        "status": "ok",
        "hostname": socket.gethostname(),
        "version": VERSION
    })

@app.route('/api/v1/secret')
def secret():
    """Protected endpoint requiring X-API-Key header."""
    if request.headers.get('X-API-Key') == API_KEY:
        return jsonify({"message": "you found the secret"})
    return jsonify({"error": "Unauthorized"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)