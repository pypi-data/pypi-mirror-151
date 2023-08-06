import sys, string
import json
import inspect 
import ast
import os
from importlib import import_module
import random
import ctypes

class ScriptGeneratorHelper:

    def begin(self, tab="\t"):
        self.code = []
        self.tab = tab
        self.level = 0

    def end(self):
        return ''.join(self.code)

    def write(self, string):
        self.code.append(self.tab * self.level + string)

    def indent(self):
        self.level = self.level + 1

    def dedent(self):
        if self.level == 0:
            raise SyntaxError("internal error in code generator")
        self.level = self.level - 1

class ScriptGenerator():
    
    def write_nginx(self, filename):
        code = ScriptGeneratorHelper()
        code.begin(tab='    ')
        code.write('worker_processes 1;\n')
        code.write('daemon off; # Prevent forking\n')
        
        code.write('pid /tmp/nginx.pid;\n')
        code.write('error_log /var/log/nginx/error.log;\n')
        
        code.write('events {\n')
        code.indent()
        code.write('# defaults\n')
        code.dedent()
        code.write('}\n')
        
        code.write('http {\n')
        code.indent()
        code.write('include /etc/nginx/mime.types;\n')
        code.write('default_type application/octet-stream;\n')
        code.write('access_log /var/log/nginx/access.log combined;\n')
        
        code.write('upstream gunicorn {\n')
        code.indent()
        code.write('server unix:/tmp/gunicorn.sock;\n')
        code.dedent()
        code.write('}\n')
        
        code.write('server {\n')
        code.indent()
        code.write('listen 8080 deferred;\n')
        code.write('client_max_body_size 5m;\n')
        code.write('keepalive_timeout 5;\n')
        code.write('proxy_read_timeout 1200s;\n')
        
        code.write('location ~ ^/(ping|invocations) {\n')
        code.indent()
        code.write('proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n')
        code.write('proxy_set_header Host $http_host;\n')
        code.write('proxy_redirect off;\n')
        code.write('proxy_pass http://gunicorn;\n')
        code.dedent()
        code.write('}\n')
        
        code.write('location / {\n')
        code.indent()
        code.write('return 404 "{}";\n')
        code.dedent()
        code.write('}\n')
        code.dedent()
        code.write('}\n')
        code.dedent()
        code.write('}\n')
        
        f = open(filename,'w')
        f.write(code.end())
        f.close()
   
    def write_serve(self, filename):
        code = ScriptGeneratorHelper()
        code.begin(tab='    ')
        code.write('#!/usr/bin/env python\n')
        code.write("# This file implements the scoring service shell. You don't necessarily need to modify it for various\n")
        code.write('# algorithms. It starts nginx and gunicorn with the correct configurations and then simply waits until\n')
        code.write('# gunicorn exits.\n')
        code.write('#\n')
        code.write('# The flask server is specified to be the app object in wsgi.py\n')
        code.write('#\n')
        code.write('# We set the following parameters:\n')
        code.write('#\n')
        code.write('# Parameter                Environment Variable              Default Value\n')
        code.write('# ---------                --------------------              -------------\n')
        code.write('# number of workers        MODEL_SERVER_WORKERS              the number of CPU cores\n')
        code.write('# timeout                  MODEL_SERVER_TIMEOUT              60 seconds\n')
       
        code.write('import multiprocessing\n')
        code.write('import os\n')
        code.write('import signal\n')
        code.write('import subprocess\n')
        code.write('import sys\n')

        code.write('cpu_count = multiprocessing.cpu_count()\n')

        code.write("model_server_timeout = os.environ.get('MODEL_SERVER_TIMEOUT', 60)\n")
        code.write("model_server_workers = int(os.environ.get('MODEL_SERVER_WORKERS', cpu_count))\n")

        code.write('def sigterm_handler(nginx_pid, gunicorn_pid):\n')
        code.indent()
        code.write('try:\n')
        code.indent()
        code.write('os.kill(nginx_pid, signal.SIGQUIT)\n')
        code.dedent()
        code.write('except OSError:\n')
        code.indent()
        code.write('pass\n')
        code.dedent()
        
        code.write('try:\n')
        code.indent()
        code.write('os.kill(gunicorn_pid, signal.SIGTERM)\n')
        code.dedent()
        code.write('except OSError:\n')
        code.indent()
        code.write('pass\n')
        code.dedent()
        
        code.write('sys.exit(0)\n')
        code.dedent()

        code.write('def start_server():\n')
        code.indent()
        code.write("print('Starting the inference server with {} workers.'.format(model_server_workers))\n")
        code.write('# link the log streams to stdout/err so they will be logged to the container logs\n')
        code.write("subprocess.check_call(['ln', '-sf', '/dev/stdout', '/var/log/nginx/access.log'])\n")
        code.write("subprocess.check_call(['ln', '-sf', '/dev/stderr', '/var/log/nginx/error.log'])\n")
        code.write("nginx = subprocess.Popen(['nginx', '-c', '/opt/program/nginx.conf'])\n")
        code.write("gunicorn = subprocess.Popen(['gunicorn',\n")
        code.indent()
        code.indent()
        code.indent()
        code.indent()
        code.indent()
        code.indent()
        code.indent()
        code.write("  '--timeout', str(model_server_timeout),\n")
        code.write("  '-k', 'sync',\n")
        code.write("  '-b', 'unix:/tmp/gunicorn.sock',\n")
        code.write("  '-w', str(model_server_workers),\n")
        code.write("  'wsgi:app'])\n")
        code.dedent()
        code.dedent()
        code.dedent()
        code.dedent()
        code.dedent()
        code.dedent()
        code.dedent()
        
        code.write('signal.signal(signal.SIGTERM, lambda a, b: sigterm_handler(nginx.pid, gunicorn.pid))\n')
        code.write('# If either subprocess exits, so do we.\n')
        code.write('pids = set([nginx.pid, gunicorn.pid])\n')
        code.write('while True:\n')
        code.indent()
        code.write('pid, _ = os.wait()\n')
        code.write('if pid in pids:\n')
        code.indent()
        code.write('break\n')
        
        code.dedent()
        code.dedent()

        code.write('sigterm_handler(nginx.pid, gunicorn.pid)\n')
        code.write("print('Inference server exiting')\n")

        code.dedent()
        code.write('# The main routine just invokes the start function.\n')
        code.write("if __name__ == '__main__':\n")
        code.indent()
        code.write('start_server()')
        
        f = open(filename,'w')
        f.write(code.end())
        f.close()

    def write_wsgi(self, filename):
        code = ScriptGeneratorHelper()
        code.begin(tab='    ')
        
        code.write('import flaskapp as myapp\n')
        code.write('# This is just a simple wrapper for gunicorn to find your app.\n')
        code.write('# If you want to change the algorithm file, simply change "predictor" above to the\n')
        code.write('# new file.\n')
        code.write('app = myapp.app')
        
        f = open(filename,'w')
        f.write(code.end())
        f.close()
        
    def write_flaskapp(self, filename, entrypoint):
        code = ScriptGeneratorHelper()
        code.begin(tab='    ')
        
        code.write('from __future__ import print_function\n')
        code.write('import io\n')
        code.write('import os\n')
        code.write('import pickle\n')
        code.write('import signal\n')
        code.write('import sys\n')
        code.write('import traceback\n')
        code.write('\n')
        code.write('import flask\n')
        code.write('from fedml_aws import Predictor\n') # changed for packaging
        code.write('\n')
        code.write('prefix = "/opt/ml/"\n')
        file, extension = entrypoint.rsplit('.', 1)
        code.write("user_module = '" + file + "'\n")
        code.write('model_path = os.path.join(prefix, "model")\n')
        
        
        code.write('class ScoringService(object):\n')
        code.indent()
        code.write("model = None  # Where we keep the model when it's loaded\n")
        code.write("predictor_obj = None  # Where we keep the model when it's loaded\n")
        code.write('\n')
        
        code.write('@classmethod\n')
        code.write('def get_predictor(cls):\n')
        code.indent()
        code.write('if cls.predictor_obj == None:\n')
        code.indent()
        code.write('cls.predictor_obj = Predictor(user_module)\n')
        code.dedent()
        code.write('return cls.predictor_obj\n')
        code.dedent()
        code.write('\n')

        code.write('@classmethod\n')
        code.write('def get_model(cls):\n')
        code.indent()
        code.write('if cls.model == None:\n')
        code.indent()
        code.write('predictor_o = cls.get_predictor()\n')
        code.write('model_fn = predictor_o.get_model_fn()\n')
        code.write('cls.model = model_fn(model_path)\n')
        code.dedent()
        code.write('return cls.model\n')
        code.dedent()
        code.write('\n')
        
        code.write('@classmethod\n')
        code.write('def transform_input(cls, input_request):\n')
        code.indent()
        code.write('predictor_o = cls.get_predictor()\n')
        code.write('input_fn = predictor_o.get_input_fn()\n')
        code.write('input_data = input_request.data.decode("utf-8")\n')
        code.write('return input_fn(input_data, input_request.content_type)\n')
        code.dedent()
        code.write('\n')
        
        code.write('@classmethod\n')
        code.write('def predict(cls, data):\n')
        code.indent()
        code.write('clf = cls.get_model()\n')
        code.write('predictor_o = cls.get_predictor()\n')
        code.write('predict_fn = predictor_o.get_predict_fn()\n')
        code.write('return predict_fn(data, clf)\n')
        code.dedent()
        code.write('\n')
        
        code.write('@classmethod\n')
        code.write('def transform_output(cls, predictions, response_content_type):\n')
        code.indent()
        code.write('predictor_o = cls.get_predictor()\n')
        code.write('output_fn = predictor_o.get_output_fn()\n')
        code.write('return output_fn(predictions, response_content_type)\n')
        code.dedent()
        code.write('\n')
        
        code.dedent()
        code.write('\n')
        code.write('# The flask app for serving predictions\n')
        code.write('app = flask.Flask(__name__)\n')
        code.write('\n')
        
        code.write('@app.route("/ping", methods=["GET"])\n')
        code.write('def ping():\n')
        code.indent()
        code.write('health = ScoringService.get_model() is not None  # You can insert a health check here\n')
        code.write('status = 200 if health else 404\n')
        code.write('return flask.Response(response="Endpoint Pinged\\n", status=status, mimetype="text/plain")\n')
        code.dedent()
        code.write('\n')
        
        code.write('@app.route("/invocations", methods=["POST"])\n')
        code.write('def transformation():\n')
        code.indent()
        code.write('data = None\n')
        code.write('data = ScoringService.transform_input(flask.request)\n')

        code.write('predictions = ScoringService.predict(data)\n')
        code.write('result = ScoringService.transform_output(predictions, str(flask.request.accept_mimetypes))\n')
        code.write("print('accept: ' + str(flask.request.accept_mimetypes))\n")
        code.write('return flask.Response(response=result, status=200, headers=None, mimetype=str(flask.request.accept_mimetypes), content_type=None, direct_passthrough=False)\n')
        
        f = open(filename,'w')
        f.write(code.end())
        f.close()
    
    def write_dockerfile(self, filename, training_image, has_requirements):
        code = ScriptGeneratorHelper()
        code.begin(tab='    ')
        
        code.write('# Build an image that can do inference on Kyma\n')
        code.write('# This is a Python 3 image that uses the nginx, gunicorn, flask stack\n')
        code.write('# for serving inferences in a stable way.\n')
        
        code.write('\n')
        code.write('FROM '+ training_image+'\n')
        code.write('\n')
        code.write('MAINTAINER FedML SAP <ci_sce@sap.com>\n')
        code.write('\n')
        code.write('\n')
        
        code.write('RUN ln -sf /usr/bin/python3 /usr/bin/python\n')
        code.write('RUN ln -sf /usr/bin/pip3 /usr/bin/pip\n')
        code.write('\n')
        
        
        code.write('ENV PYTHONUNBUFFERED=TRUE\n')
        code.write('ENV PYTHONDONTWRITEBYTECODE=TRUE\n')
        code.write('ENV PATH="/opt/program:${PATH}"\n')
        
        code.write('\n')
        code.write('COPY SKLearn /opt/program\n')
        code.write('COPY ml /opt/ml\n')
        # code.write('COPY pack /opt/pack\n') # commented out when published for packaging on pypi
        code.write('WORKDIR /opt/program\n')
        code.write('\n')
        
        if has_requirements == True:
            code.write('RUN pip --no-cache-dir install -r /opt/program/source/requirements.txt\n')
            code.write('\n')
        code.write('\n')
        
        # TODO : Change for PIP INSTALL pypi instead of whl
        # code.write('RUN pip install /opt/pack/fedml_aws-2.0.0-py3-none-any.whl\n')
        code.write('RUN pip install fedml-aws\n')

        code.write('CMD ["serve"]')
        
        f = open(filename,'w')
        f.write(code.end())
        f.close()
        
    def write_deployment(self, filename, foldername, num_instances, container_image, profile_name):
        code = ScriptGeneratorHelper()
        code.begin(tab='    ')
        
        code.write('apiVersion: v1\n')
        code.write('kind: Service\n')
        code.write('metadata:\n')
        code.write('  name: '+foldername+'\n')
        code.write('  labels:\n')
        code.write('    run: '+foldername+'\n')
        code.write('spec:\n')
        code.write('  ports:\n')
        code.write('  - name: http\n')
        code.write('    port: 8080\n')
        code.write('  selector:\n')
        code.write('    run: '+foldername+'\n')
        code.write('\n')
        code.write('---\n')
        code.write('\n')
        code.write('apiVersion: apps/v1\n')
        code.write('kind: Deployment\n')
        code.write('metadata:\n')
        code.write('  name: '+foldername+'\n')
        code.write('  labels:\n')
        code.write('    run: '+foldername+'\n')
        code.write('spec:\n')
        code.write('  selector:\n')
        code.write('    matchLabels:\n')
        code.write('      run: '+foldername+'\n')
        code.write('  replicas: '+str(num_instances)+'\n')
        code.write('  template:\n')
        code.write('    metadata:\n')
        code.write('      labels:\n')
        code.write('        run: '+foldername+'\n')
        code.write('    spec:\n')
        code.write('      imagePullSecrets:\n')
        code.write('        - name: '+profile_name+'-aws-ecr\n')
        code.write('      containers:\n') 
        code.write('        - image: '+container_image)
        code.write('\n')
        code.write('          name: '+foldername+'\n')
        code.write('          ports:\n')
        code.write('          - containerPort: 8080\n')
        code.write('\n')
        code.write('---\n')
        code.write('\n')
        code.write('apiVersion: gateway.kyma-project.io/v1alpha1\n')
        code.write('kind: APIRule\n')
        code.write('metadata:\n')
        code.write('  name: '+foldername+'\n')
        code.write('spec:\n')
        code.write('  gateway: kyma-gateway.kyma-system.svc.cluster.local\n')
        code.write('  service:\n')
        code.write('    name: '+foldername+'\n')
        code.write('    port: 8080\n')
        code.write('    host: '+foldername+'\n')
        code.write('  rules:\n')
        code.write('    - path: /.*\n')
        code.write('      methods: ["GET", "POST"]\n')
        code.write('      mutators: []\n')
        code.write('      accessStrategies:\n')
        code.write('        - handler: noop\n')
        code.write('          config: {}\n')
        
        
        f = open(filename,'w')
        f.write(code.end())
        f.close()