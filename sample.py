import serial
import requests
import sys

def send_sample(device, endpoint):
    with serial.Serial(device) as ser:
        value = int(ser.read(3))
        res = requests.post(endpoint, json=dict(
            value=value,
            labels=dict(
                sensor='test01'
            )
        ))

if __name__ == '__main__':
    if len(sys.argv) == 3:
        device = sys.argv[1]
        endpoint = sys.argv[2]

        send_sample(device, endpoint)
    else:
        print('Usage: {} DEVICE ENDPOINT'.format(sys.argv[0]))