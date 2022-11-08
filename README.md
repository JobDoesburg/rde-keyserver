# RDE KeyServer
This repository contains the RDE KeyServer. The KeyServer is a simple Django application that provides a public key 
register for RDE keys. It provides a simple web interface that allows users to register their public keys. The KeyServer 
also provides a REST API that allows other applications to retrieve the public keys of users, based on their email 
address. User authentication is handled via SAML.

## Installation
Probably you want to use the [RDE POC server config](https://gitlab.surf.nl/filesender/rde-poc-server-config) repository
to install the KeyServer. If you want to install the KeyServer manually, follow these steps:

1. Install docker: `sudo apt install docker`
2. Clone this repository: `git clone git@gitlab.surf.nl:filesender/rde-keyserver.git`
3. Verify the settings in `keyserver/settings.py`. In particular, you should set the `SAML2_AUTH` settings to match 
   your SAML2 IdP.
    - Have a look at the [Django-SAML2-Auth documentation](https://djangosaml2.readthedocs.io/contents/setup.html#configuration) 
      for more information on the `SAML2_AUTH` settings.
    - Create the SSL certificate and key for the KeyServer SAML SP. The certificate and key should be placed in the 
      `keyserver/config/saml` directory. The certificate should be named `public.cert` and the key should be named 
      `private.key`. They can be generated using the following commands: 
      `openssl req -nodes -new -x509 -newkey rsa:2048 -days 3650 -keyout private.key -out public.cert`.
      These files can also be mounted into the container using a docker volume.
4. Build the docker image: `docker build -t rde-keyserver .`
5. Run the docker image: `docker run -p 8000:8000 rde-keyserver`

The KeyServer should now be running on port 8000. You can access the web interface at `http://localhost:8000/`. 
Static (and media) directories are not hosted by this server, so you will need to configure a web server to serve. 
These directories are available at `/code/static` and `/code/media` respectively and can be mounted as volumes.

You probably also want to mount the `keyserver/config/saml` directory as a volume, so that you can easily replace the
SAML SP certificate and key, and the `keyserver/db.sqlite3` file as a volume. This will allow you to persist the db.