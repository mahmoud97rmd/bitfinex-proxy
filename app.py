from flask import Flask, request, Response
import requests

app = Flask(__name__)

BF_BASE = 'https://api-pub.bitfinex.com'

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    url = f"{BF_BASE}/{path}"
    if request.query_string:
        url += '?' + request.query_string.decode()
    
    try:
        r = requests.get(url, headers={
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }, timeout=10)
        
        return Response(
            r.content,
            status=r.status_code,
            headers={
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        )
    except Exception as e:
        return Response('{"error":"proxy_error"}', status=500,
                       headers={'Content-Type': 'application/json'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
