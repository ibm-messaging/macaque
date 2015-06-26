#Copyright (c) 2014 IBM Corporation.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v10.html
#
# Contributors:
# IBM - initial implementation
import macaque
import os, json
import uuid
from time import sleep

service_address = 'mqlight/sample/wordsuppercase'
SHARE_ID = 'python-back-end'
CLIENT_ID = 'python_backend_' + str(uuid.uuid4()).replace('-', '_')[0:7]

if os.environ.get('VCAP_SERVICES'):
    vcap_services = os.environ.get('VCAP_SERVICES')
    decoded = json.loads(vcap_services)['mqlight'][0]

    service = str(decoded['credentials']['connectionLookupURI'])
    username = str(decoded['credentials']['username'])
    password = str(decoded['credentials']['password'])
    security_options = {
        'property_user': username,
        'property_password': password
    }
else:
    service = 'amqp://127.0.0.1:5672'
    security_options = {}

app = macaque.Server(broker = service, cid = CLIENT_ID, security_options = security_options)

@app.service(service_address, share_id = SHARE_ID)
def process_message(data):
    print data
    word = data['word']
    reply_data = {
    	'word': word.upper(),
    	'backend': 'Python: ' + CLIENT_ID
    }
    return reply_data


if __name__ == '__main__':
    try:
    	while True:
    		sleep(1)
    except KeyboardInterrupt:
    	pass
