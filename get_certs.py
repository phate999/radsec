# get_certs - decrypt certificates from NCOS for use
from csclient import EventingCSClient
import json
cp = EventingCSClient('get_certs')
cp.log('Starting...')

# Get radsecproxy.conf from config/hotspot/tos/text
conf = cp.get('config/hotspot/tos/text')
try:
    with open('/etc/radsecproxy.conf', 'wt') as f:
        f.write(conf)
        cp.log('Found radsecproxy.conf in /config/hotspot/tos/text and wrote to /etc/radsecproxy.conf')
except:
    cp.log('Paste radsecproxy.conf into Hotspot TOS - /config/hotspot/tox/text')

# Get certs from config/certmgmt/certs
certs = cp.get('config/certmgmt/certs')
found = {"cert": False, "key": False, "CA": False}
for cert in certs:
    if 'Zscaler' not in cert["name"]:
        if 'client' in cert["name"].lower():
            with open('/etc/pki/radsecproxy/radsec-client-cert.pem', 'wt') as f:
                f.write(cert["x509"])
                found["cert"] = True
                cp.log(f'Found Client Certificate: {cert["name"]} and wrote to /etc/pki/radsecproxy/radsec-client-cert.pem')
            with open('/etc/pki/radsecproxy/radsec-client-key.pem', 'wt') as f:
                key = cp.decrypt(f'config/certmgmt/certs/{cert["_id_"]}/key')
                f.write(key)
                found["key"] = True
                cp.log(f'Found Client Key: {cert["name"]} and wrote to /etc/pki/radsecproxy/radsec-client-key.pem')
        elif 'ca' in cert["name"].lower():
            with open('/etc/pki/radsecproxy/ca.pem', 'wt') as f:
                f.write(cert["x509"])
                found["CA"] = True
                cp.log(f'Found CA: {cert["name"]} and wrote to /etc/pki/radsecproxy/ca.pem')
if False in found.values():
    cp.log('*** MISSING RADSEC CERTIFICATES ***')
    cp.log('Import CA Certificate with "ca" in title.  Import client certificate with "client" in title.')
else:
    cp.log(f'Found all RadSec Certificiates.')
cp.log(f'Found: {json.dumps(found).strip("{}")}')

