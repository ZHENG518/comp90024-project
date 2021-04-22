from flask import Flask, jsonify, request, g
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/test', methods=['GET'])
def test():
    try:
        name = request.args.get("name")
        return jsonify({
            'code': 1000,
            'data': f'Hello,{name}!'
        })
    except Exception as e:
        return jsonify({'code': 2000, 'message': 'error'})

    
if __name__ == '__main__':
    app.run(host="0.0.0.0")