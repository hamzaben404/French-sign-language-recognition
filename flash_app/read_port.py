import serial
import time

def read_from_serial(serial_port):
    try:
        arduino = serial.Serial(serial_port, baud_rate)
        while True:
            if arduino.in_waiting > 0:
                line = arduino.readline().decode('utf-8').strip()
                print(f"Received data: {line}")
            time.sleep(0.1)  # Attente courte entre les lectures pour éviter de surcharger le port série
    except serial.SerialException as e:
        print(f"Serial error: {e}")

if __name__ == "__main__":
    serial_port = '/dev/ttyUSB0'
    baud_rate = 9600
    read_from_serial(serial_port)
