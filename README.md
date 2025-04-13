# French Sign Language Recognition with Smart Gloves

A system that recognizes French sign language gestures using smart gloves with flex sensors and motion tracking.

## Project Overview

This project is a sophisticated sign language recognition system that uses sensor-equipped smart gloves to interpret French Sign Language gestures in real-time. The system combines hardware sensors, machine learning, and a web interface to create an accessible communication tool for sign language users.

### Key Features

- **Smart Gloves Hardware**: Equipped with flex sensors that measure finger bending and an MPU6050 motion sensor that captures hand orientation and movement
- **Real-time Recognition**: Processes sensor data to recognize sign language gestures as they're performed
- **BiLSTM Neural Network**: Uses a Bidirectional Long Short-Term Memory neural network specifically trained to recognize sequential hand movement patterns
- **Text-to-Speech Output**: Converts recognized signs into spoken French using Google's Text-to-Speech technology
- **Web Interface**: Displays the recognized signs and provides audio playback

## Project Components

The project consists of three main components:

1. **Hardware (Arduino)**
   - Arduino Mega board
   - 6 flex sensors for finger position sensing
   - MPU6050 for accelerometer and gyroscope data
   - Wiring as specified in the Arduino code

2. **Data Processing & ML (Python)**
   - BiLSTM neural network model (model_bilstm.h5)
   - Data preprocessing and normalization
   - Prediction confidence threshold system
   - Text-to-speech conversion

3. **Web Interface**
   - Flask backend API
   - React frontend application
   - Real-time display of recognized signs

## Setup Instructions

### Hardware Setup

1. Connect the flex sensors to analog pins A0-A5 on the Arduino
2. Connect the MPU6050 sensor to the I2C pins (SDA/SCL)
3. Upload `main.ino` to the Arduino

### Software Requirements

- Python 3.7+
- Node.js and npm
- Required Python packages:
  - tensorflow
  - pandas
  - numpy
  - scikit-learn
  - gtts
  - pyserial
  - flask
  - flask-cors

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/french-sign-language-gloves.git
   cd french-sign-language-gloves
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure the serial port in `app.py`:
   - For Windows: Change `serial_port = '/dev/ttyUSB1'` to `serial_port = 'COM3'` (or your Arduino port)
   - For Mac: Change to `serial_port = '/dev/tty.usbserial-XXXX'` (find your port with `ls /dev/tty.*`)

5. Install web app dependencies:
   ```
   cd plbd20-app
   npm install
   ```

### Running the Application

1. Connect the Arduino to your computer

2. Start the Flask backend server:
   ```
   python backend.py
   ```

3. In a separate terminal, start the web application:
   ```
   cd plbd20-app
   npm start
   ```

4. Open your browser and navigate to `http://localhost:3000`

## Data Collection and Training

To collect data for new signs:

1. Edit the `capturer.py` file to set the appropriate label for the sign
2. Run `python capturer.py` and perform the sign multiple times
3. The data will be saved to a CSV file

To retrain the model:
1. Organize your collected data
2. Use the BiLSTM architecture to train on the new data
3. Replace the `model_bilstm.h5` and `label_encoder.pkl` files

## Troubleshooting

- **Serial Connection Issues**: Verify the correct port is selected and that the Arduino is connected
- **Model Not Working**: Check that the data format matches the expected input structure (50 samples x 11 features)
- **Web App Not Displaying**: Ensure the Flask backend is running and accessible

## Architecture Diagram

```
+---------------+          +------------------+          +---------------+
|               |  Serial  |                  |   API    |               |
|   Smart       |--------->|   Python         |--------->|   Web         |
|   Gloves      |  Data    |   Backend        |   JSON   |   Interface   |
|   (Arduino)   |          |   (Flask)        |          |   (React)     |
+---------------+          +------------------+          +---------------+
                                   |
                                   | Prediction
                                   v
                           +------------------+
                           |                  |
                           |   BiLSTM Model   |
                           |                  |
                           +------------------+
```

## Future Improvements

- Add support for a wider range of signs and phrases
- Implement a mobile application interface
- Improve model accuracy with more training data
- Add gesture combination for forming complete sentences


## Acknowledgements

This project was originally created by Benkirane Mokhtar & Benatmane Hamza.

