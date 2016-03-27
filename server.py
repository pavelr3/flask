#!flask/bin/python
from flask import Flask, request, jsonify
import json
from elasticsearch import Elasticsearch
import random

app = Flask(__name__)
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


@app.route('/measurements', methods=['GET', 'POST'])
def handle_measurements():
    if request.method == 'POST':
        return prepare_measurements()
    else:
        return jsonify(contents=get_measurements())


def prepare_measurements():
    if not request.json or 'num' not in request.json:
        pass
    else:
        num = request.json['num']
        print "Adding %s instances of data" % num

        if not es.indices.exists("geo"):
            es.indices.create(index="geo", body={
                                            "mappings": {
                                                "location": {
                                                    "properties": {
                                                        "value": {"type": "string"},
                                                        "pin": {"type": "geo_point"}
                                                    }
                                                }
                                            }})
        for i in xrange(num):
            # Prepare values
            value = random.randint(0, 99)
            geo = {"lat": random.uniform(-100, 100), "lon": random.uniform(-100, 100)}
            # Insert to elasticsearch
            res = es.index(index="geo", doc_type="location", body={"value": value, "pin": geo})
            print('Added: ', res['created'])
    return 'OK'


def get_measurements():
    # Get params for the URL
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    radius = request.args.get("radius")

    # Search in elasticsearch for the values received
    res = es.search(index="geo", doc_type="pin", body={"filter": {
                                                                    "geo_distance": {
                                                                        "distance": '%skm' % radius,
                                                                        "pin": {
                                                                            "lat": lat,
                                                                            "lon": lon
                                                                        }
                                                                        }
                                                                    },
                                                               "query": {
                                                                    "match_all": ()
                                                                }
                                                               })
    return res['hits']['hits']

if __name__ == '__main__':
    app.run(debug=True)
