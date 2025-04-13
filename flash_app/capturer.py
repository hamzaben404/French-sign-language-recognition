import serial
import time
import csv

# Configuration du port série (ajuste selon tes besoins)
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Spécifie le chemin complet du port série et configure le timeout
print("Ca va commencer dans 2 secondes...")
time.sleep(3)  # Donne du temps à la connexion pour s'établir

n_samples = 50  # Nombre d'échantillons
n_lines = 50  # Nombre de lignes par échantillon (nombre de mesures par échantillon)

# Configuration du fichier CSV
filename = 'abder.csv'
features = ["label", "auriculaire", "pouce", "majeur", "anuleur", "index", "acx", "acy", "acz", "gyx", "gyy", "gyz"]

with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(features)  # Écrire les en-têtes

    for i in range(n_samples):
        for j in range(n_lines):
            ser.flush()
            line = ser.readline().decode('utf-8').strip()
            data_values = line.split('\t')

            # Compléter les données par des zéros si nécessaire
            if len(data_values) < 11:
                data_values += ['0'] * (11 - len(data_values))
            elif len(data_values) > 11:
                data_values = data_values[:11]


            # Écrire dans le fichier CSV avec le label '1'
            writer.writerow([1] + data_values)
            time.sleep(0.04)

        print(f"Fin de l'échantillon {i + 1}/{n_samples}")
        writer.writerow("===========================================================================")
        print("vous allez attendre 2 seconde............................")
        time.sleep(3)  # Pause de 2 secondes entre les échantillons
        print("ca y est --------------------------------------------")
        time.sleep(0.1)

print("Terminé !===========================================================")

ser.close()
