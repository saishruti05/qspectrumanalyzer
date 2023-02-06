from flask import Flask, jsonify, request
import numpy as np
import serial

app = Flask(name)

# Open a serial connection to the device
ser = serial.Serial("COM4", 115200)

@app.route('/iq_data', methods=['GET'])
def get_iq_data():
    # Send a command to the device to retrieve IQ data
    ser.write(b'get_iq_data\n')
    # Read the IQ data from the device
    iq_data = ser.readline()
    # Convert the data to a numpy array
    iq_data = np.fromstring(iq_data, dtype=np.complex64)
    return jsonify({'iq_data': iq_data.tolist()})

@app.route('/fft_data', methods=['GET'])
def get_fft_data():
    # Send a command to the device to retrieve IQ data
    ser.write(b'get_iq_data\n')
    # Read the IQ data from the device
    iq_data = ser.readline()
    # Convert the data to a numpy array
    iq_data = np.fromstring(iq_data, dtype=np.complex64)
    # Perform FFT on the IQ data
    fft_data = np.fft.fft(iq_data)
    return jsonify({'fft_data': fft_data.tolist()})

if name == 'main':
    app.run(debug=True)