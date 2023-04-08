from flask import Flask,request,jsonify
import os
import subprocess

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
    os.system("az login -u "+username+" -p "+password)
    os.system("az webapp create  --resource-group "+resourceGroup+" --plan  "+ plan +"--name "+branch+" ---multicontainer-config-type compose --multicontainer-config-file /usr/src/app/src/ALLINONE/docker-compose.yml")
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
