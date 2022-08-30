# How to Use: RadSecProxy for Cradlepoint routers  

Use the container image: phate999/radsec  

# Project on Docker Hub:  
https://hub.docker.com/r/phate999/radsec

## radsecproxy.conf
Modify the below radsecproxy.conf for your RADIUS servers and paste into the Cradlepoint's Hotspot TOS text (**/config/hotspot/tos/text/**).  Do not change the paths of the certificate files.

```conf
tls default {
    CACertificateFile	/etc/pki/radsecproxy/ca.pem
    CertificateFile	/etc/pki/radsecproxy/radsec-client-cert.pem
    CertificateKeyFile	/etc/pki/radsecproxy/radsec-client-key.pem
    TlsVersion TLS1_2
}

server radius1.mydomain.com {
	type TLS
	port 2083
	tls default
	TCPKeepalive on
	StatusServer on
	CertificateNameCheck on
}

server radius2.mydomain.com {
	type TLS
	port 2083
	tls default
	TCPKeepalive on
	StatusServer on
	CertificateNameCheck on
}

realm * {
	server radius1.mydomain.com
	server radius2.mydomain.com
}

client 127.0.0.1 {
	type	udp
	secret	testing123
}

LogLevel		5
LogDestination		file:///var/log/radsecproxy/radsecproxy.log
```

## Import Certificates

- Import your CA certificate into the Cradlepoint's Certificate Manager with "ca" in the title (e.g. "my_ca_cert").
- Import your client certificate into the Cradlepoint's Certificate Manager with "client" in the title (e.g. "my_client_cert").

## Setup Container

- Add a new container project named "radsec" and paste in the compose below:

```yaml
version: '2.4'
services:
  radsec:
    image: 'phate999/radsec'
    ports:
     - '1812:1812'
     - '1813:1813'
    volumes:
     - ${CONFIG_STORE}
```

### On container startup, the radsecproxy.conf file and certificates will be pulled from the router configuration and used to start the radsecproxy service.

Check the Cradlepoint router logs for status.
