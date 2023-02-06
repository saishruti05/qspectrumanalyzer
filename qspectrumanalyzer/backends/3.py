import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation
import serial
from flask import Flask, jsonify, request

app = Flask(__name__)

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

    # Implement noise reduction processing on the IQ data
    iq_data = np.real(iq_data)
    iq_data = np.maximum(iq_data - 0.1, 0)

    return jsonify({'iq_data': iq_data.tolist()})

RATE = 44100
BUFFER = 882

#
fig = plt.figure()
line1 = plt.plot([],[])[0]
line2 = plt.plot([],[])[0]

r = range(0,int(RATE/2+1),int(RATE/BUFFER))
l = len(r)

def init_line():
        line1.set_data(r, [-1000]*l)
        line2.set_data(r, [-1000]*l)
        return (line1,line2,)

def update_line(i, data):
    data = np.log10(np.sqrt(np.real(data)*2+np.imag(data)*2) / BUFFER) * 10
    line1.set_data(r, data)
    line2.set_data(np.maximum(line1.get_data(), line2.get_data()))
    return (line1,line2,)

plt.xlim(0, RATE/2+1)
plt.ylim(-60, 0)
plt.xlabel('Frequency')
plt.ylabel('dB')
plt.title('Spectrometer')
plt.grid()

if __name__ == '_main_':
    # Send a command to the device to retrieve IQ data
    ser.write(b'get_iq_data\n')
    # Read the IQ data from the device
    iq_data = ser.readline()
    # Convert the data to a numpy array
    iq_data = np.fromstring(iq_data, dtype=np.complex64)
    # Perform FFT on the IQ data
    fft_data = np.fft.fft(iq_data)

    line_ani = matplotlib.animation.FuncAnimation(
        fig, update_line, fargs=(fft_data,), interval=0, init_func=init_line, blit=True
    )

    plt.show()