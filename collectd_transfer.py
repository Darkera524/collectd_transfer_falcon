from flask import Flask
from flask import jsonify
from flask import request
import requests
import json

app = Flask(__name__)

##ts=`date +%s`; curl -X POST -d "[{\"metric\": \"metric.demo\", \"endpoint\": \"qd-open-falcon-judge01.hd\", \"timestamp\": $ts,\"step\": 60,\"value\": 9,\"counterType\": \"GAUGE\",\"tags\": \"project=falcon,module=judge\"}]" http://127.0.0.1:1988/v1/push
@app.route('/collectd_tranfer', methods=['POST'])
def transfer():
    ip = request.remote_addr
    json_data = json.loads(request.data.decode())
    falcon_list = []
    for item in json_data:
        endpoint_ins = item.get('host').split(".")
        endpoint = endpoint_ins[0]

        ins_data = {
            "metric": item.get("plugin") + "." + item.get('type'),
            "endpoint": endpoint,
            "timestamp": int(item.get("time")),
            "step": 60,
            "value": item.get("values")[0],
            "counterType": "GAUGE",
        }

        if item.get("type_instance") != "":
            ins_data["tags"] = "type_instance=" + item.get("type_instance")
        else:
            ins_data["tags"] = ""

        falcon_list.append(ins_data)

    urlto = "http://"+ip+":1988/v1/push"

    headerdata = {"Content-Type": "application/json"}
    r = requests.post(urlto, data=json.dumps(falcon_list))
    response = r.text
    print(response)

    return jsonify({"ret": 1})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port="5001")
