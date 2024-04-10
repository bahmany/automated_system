import json

import airflow_python_sdk
import requests
from requests.auth import HTTPBasicAuth


class AirflowConnector:
    url = 'http://localhost:8080/api/v1/'
    auth = HTTPBasicAuth('admin', 'VEUK9PbvPWeR33YX')



    def get_list(self, command_name):
        result = requests.get(self.url + command_name, auth=self.auth).content
        result = json.loads(result)
        return result

    def get_one(self, command_name, id):
        return requests.get(self.url + command_name + "/" + id, auth=self.auth)

    def add_one(self, command_name, json_form):
        return requests.post(self.url + command_name, auth=self.auth, json=json_form,
                             headers={"Content-Type": "application/json", "Accept": "application/json"})

    def post(self, command_name, json_form):
        return requests.post(self.url + command_name, auth=self.auth, json=json_form,
                             headers={"Content-Type": "application/json", "Accept": "application/json"})
