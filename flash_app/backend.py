# flask_app.py
from flask import Flask, jsonify, send_file
from flask_cors import CORS
from app import contloop

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Route pour récupérer la prédiction sous forme de JSON
@app.route('/api/prediction', methods=['GET'])
def get_prediction():
    prediction, audio_base64 = contloop()
    print("Prediction: ", prediction)
    return jsonify({'prediction': prediction, 'audio': audio_base64})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
