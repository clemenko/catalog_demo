from flask import Flask, render_template, request, jsonify, redirect, url_for

import os
import requests
import json

version = "0.1"
app = Flask(__name__)

@app.route('/token', methods=['GET'])
def get_token():
        # Define the cURL request parameters
    url = "https://rancher.rfed.me/v3-public/localProviders/local?action=login"
    payload = {"username":"admin","password":"Pa22word"}
    headers = {'Content-Type': 'application/json'}
    
    # Send the cURL request using the requests library
    response = requests.post(url, json=payload, headers=headers, verify=False)
    
    # Return the response from the web server
    jraw=response.text
    raw = json.loads(jraw)
    token = (raw["token"])
    return token

@app.route('/', methods=['GET', 'POST'])
def send_curl():
    if request.method == 'POST':
        token = get_token()
        
        url = "https://rancher.rfed.me/v1/catalog.cattle.io.clusterrepos/kpa?action=install"
        
        payload = {"charts":[{"chartName":"tetris","version":"0.1.9","releaseName":"tetris","annotations":{"catalog.cattle.io/ui-source-repo-type":"cluster","catalog.cattle.io/ui-source-repo":"kpa"},"values":{"global":{"cattle":{"clusterId":"local","clusterName":"local","systemDefaultRegistry":"","systemProjectId":"p-c95sg","url":"https://rancher.rfed.me","rkePathPrefix":"","rkeWindowsPathPrefix":""},"systemDefaultRegistry":""}}}],"timeout":"600s","namespace":"tetris"}

        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}', 'accept': 'application/json', 'accept-language': 'en-US,en;q=0.9', 'content-type': 'application/json;charset=UTF-8'}
        
        # Send the cURL request using the requests library
        response = requests.post(url, json=payload, headers=headers, verify=False)   

        return response.text, 200
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False)
