from flask import Flask, request, jsonify
import threading

app = Flask(__name__)
bots = {}

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    bot_id = data['bot_id']
    bots[bot_id] = data
    return jsonify({"status": "success"})

@app.route('/command', methods=['POST'])
def command():
    data = request.json
    bot_id = data['bot_id']
    command = data['command']
    if bot_id in bots:
        # Envoyer la commande au bot
        return jsonify({"status": "success"})
    return jsonify({"status": "failure"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)