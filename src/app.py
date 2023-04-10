from flask import Flask,request,jsonify
import os
import subprocess
#from passlib.hash import sha256_crypt
import hmac
import hashlib
import base64
from functools import wraps
def checkHeader():
    def _home_decorator(f):
        @wraps(f)
        def __home_decorator(*args, **kwargs):
            data = request.get_data()
            header = request.headers['X-Hub-Signature-256']
            token = header.split('=')[-1]
            print("token="+token,flush=True)
            print(os.environ['SECRET_TOKEN'],flush=True)
            # Why 8eda83011fcc8f66e9eda1a980fbd09bdea4dc1b5e63693049773ecbde82a0d3 is not valid sha256_crypt hash?
            digest = hmac.new(os.environ['SECRET_TOKEN'].encode('utf-8'), data, digestmod=hashlib.sha256).digest()
            computed_hmac = base64.b64encode(digest)
            if not hmac.compare_digest(computed_hmac, token.encode('utf-8')) :
                print("not ok",flush=True)
                return jsonify({"message": "Not Authorized"}), 401  
            print(header,flush=True)
            all_headers = request.headers
            print(all_headers,flush=True)
            return f(*args, **kwargs)
        return __home_decorator
    return _home_decorator

app = Flask(__name__)

@app.route('/github', methods=['POST'])
def githun():
    obj = request.json
    resourceGroup = os.environ['RESOURCE_GROUP']
    plan = os.environ['PLAN_NAME']
    username= os.environ['USERNAME']
    password= os.environ['PASSWORD']
    
    branch = obj['ref'].split('/')[-1]
    print(branch,flush=True)
    os.system("cd /usr/src/app/src/ALLINONE/ && git checkout "+branch+" && git pull && git submodule update")
    #os.system("az login -u "+username+" -p "+password)
    #os.system("az webapp create  --resource-group "+resourceGroup+" --plan  "+ plan +"--name "+branch+" ---multicontainer-config-type compose --multicontainer-config-file /usr/src/app/src/ALLINONE/docker-compose.yml")
    return "ok"

@app.route('/github_delete',methods=['POST'])
def github_delete():
    obj = request.json
    print(obj,flush=True)
    branch = obj['ref'].split('/')[-1]
    resourceGroup = os.environ['RESOURCE_GROUP']
    username= os.environ['USERNAME']
    password= os.environ['PASSWORD']

    os.system("az login -u "+username+" -p "+password)
    os.system("az webapp delete --name"+branch+"--resource-group "+resourceGroup)
    os.system("cd /usr/src/app/src/ALLINONE/ && git checkout dev && git pull && git submodule update")
    return "ok"
