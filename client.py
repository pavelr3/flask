import requests
import json


def generate(num):
    payload = {'num': num}
    headers = {'content-type': 'application/json'}
    requests.post('http://127.0.0.1:5000/measurements', data=json.dumps(payload), headers=headers)


def get(radius, location):
    hist = {(i, 0) for i in xrange(10)}
    getmsg = 'http://127.0.0.1:5000/measurements?lat=%s&lon=%s&radius=%s' % (location['lat'], location['lon'], radius)
    res = requests.get(getmsg)


if __name__ == '__main__':
    # send get request
    generate(5)
    # get(50, {"lat": 10, "lon": 10})
