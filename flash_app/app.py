import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
from gtts import gTTS
import random, string, os, time, serial, pickle, io, base64


def generate_random_text(length=10):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


# Désactiver l'utilisation des GPU
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# Nombre d'échantillons attendus par le modèle
n_echantillon = 50
n_features = 11
# Charger le modèle Bi-LSTM
model = load_model('model_bilstm.h5')

# Charger le LabelEncoder
with open('label_encoder.pkl', 'rb') as file:
    label_encoder = pickle.load(file)

# Configuration de la connexion série
serial_port = '/dev/ttyUSB1'  # Remplacer par le port série de l'Arduino
baud_rate = 9600  # Correspond à la vitesse de communication définie dans l'Arduino
chemin_csv = "data_frame.csv"


# Lire directement un texte
def sound_function(predictions):
    tts = gTTS(text=predictions, lang='fr')
    audio_file = "prediction.mp3"
    tts.save(audio_file)
    os.system(f"mpg321 {audio_file}")
    os.remove(audio_file)  # Supprimer le fichier après lecture


# Générer du son
def generate_sound(predictions):
    tts = gTTS(text=predictions, lang='fr')
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    audio_base64 = base64.b64encode(audio_buffer.read()).decode('utf-8')
    return audio_base64


def predire(data):
    prediction = model.predict(data)
    predicted_class_index = np.argmax(prediction, axis=1)
    taux_confiance = np.max(prediction, axis=1)
    print("taux de confiance ...", taux_confiance)
    if taux_confiance < 0.6:
        return ''
    predicted_label = label_encoder.inverse_transform(predicted_class_index)
    return predicted_label[0]


# Préparer les données
def prepare_smart_glove_data_for_prediction(data, max_seq_len=50):
    # Convertir les données en DataFrame
    df = pd.DataFrame(data)

    # Remplacer les valeurs non convertibles par NaN et remplir les valeurs manquantes par la moyenne
    df = df.apply(pd.to_numeric, errors='coerce').fillna(df.mean())

    # Vérifier et ajuster le nombre de colonnes
    expected_features = 11  # Nombre de fonctionnalités attendu par le modèle
    if df.shape[1] > expected_features:
        df = df.iloc[:, :expected_features]  # Troncature des colonnes supplémentaires
    elif df.shape[1] < expected_features:
        for _ in range(expected_features - df.shape[1]):
            df[f'new_col_{_}'] = 0.0  # Ajout de colonnes manquantes avec des zéros

    # Convertir les données en numpy array
    data = df.to_numpy()

    # Assurer que les données ont la longueur maximale de séquence
    if data.shape[0] < max_seq_len:
        # Padding
        padding = np.zeros((max_seq_len - data.shape[0], data.shape[1]))
        data = np.vstack((data, padding))
    elif data.shape[0] > max_seq_len:
        # Truncating
        data = data[:max_seq_len, :]

    # Reshaper les données pour qu'elles soient compatibles avec le modèle BiLSTM
    X = data.reshape(1, max_seq_len, data.shape[1])

    return X


# Conversion en float
def convertir_float(s):
    try:
        return float(s)
    except ValueError:
        return 0.0


def adjuster_data(data, n_echantillon):
    while len(data) < n_echantillon:
        data.append([0.0] * len(data[0]))
    max_length = max(len(lst) for lst in data)
    for i in range(len(data)):
        if len(data[i]) < max_length:
            data[i].extend([0.0] * (max_length - len(data[i])))
    return data


# Fonction principale pour la capture des données et la prédiction
def contloop():
    arduino = serial.Serial(serial_port, baud_rate)  # Initialise la connexion série avec l'Arduino
    count = 0
    data = []

    while count < n_echantillon:
        arduino.flush()
        try:
            line = arduino.readline().strip()  # Lire une ligne de données de l'Arduino
            line = line.decode('utf-8').split('\t')
            liste = [convertir_float(elem) for elem in line]
            data.append(liste)
            count += 1
        except UnicodeDecodeError:
            print("Erreur de décodage, ligne ignorée")
        time.sleep(0.04)

    data = adjuster_data(data, n_echantillon)

    X = prepare_smart_glove_data_for_prediction(data)
    # Faire la prédiction
    y_pred = model.predict(X)
    # Convertir la prédiction en label
    y_pred_label = np.argmax(y_pred, axis=1)
    # Afficher le résultat
    predictions = label_encoder.inverse_transform(y_pred_label)[0]

    audio_base64 = generate_sound(predictions)
    print(predictions)  # Affiche les prédictions
    # sound_function(predictions)  # Convertit les prédictions en sortie vocale (à implémenter)
    return predictions, audio_base64



if __name__ == '__main__':
    while(True):
        contloop()
