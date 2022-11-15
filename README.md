# RDE KeyServer
This repository contains the RDE KeyServer. This key server is a simple Django application that provides a public key 
register for RDE keys. It provides a simple web interface that allows users to register their public keys. The key
server also provides a REST API that allows other applications to retrieve the public keys of users, based on their 
email address. User authentication is handled via SAML.

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

The key server should now be running on port 8000. You can access the web interface at `http://localhost:8000/`. 
Static (and media) directories are not hosted by this server, so you will need to configure a web server to serve. 
These directories are available at `/code/static` and `/code/media` respectively and can be mounted as volumes.

You probably also want to mount the `keyserver/config/saml` directory as a volume, so that you can easily replace the
SAML SP certificate and key, and the `keyserver/db.sqlite3` file as a volume. This will allow you to persist the db.

## API

### Search for a public key (enrollment parameters)
The KeyServer provides a REST API that allows other applications to retrieve the public keys of users, based on their
email address. This API can be queries using `/api/search?email=<email>`. The API will return a JSON object with the 
enrollment parameters for the user with the given email address. If no user is found, the API will return a 404 error.

### Register an RDE document
The KeyServer also provides a REST API that allows users to register their RDE documents. This API can be queries using
`/api/enroll/<ticket>/`. Here the `<ticket>` should be replaced with the ticket that was generated by the key server 
when the user requests to register a new RDE document (via the frontend). The API expects a JSON object with the 
enrollment parameters for the RDE document and will return these parameters if the enrollment was successful.

## Usage
The KeyServer provides a simple web interface that allows users to view and register their RDE documents. The web 
interface is protected by SAML authentication. Users can register a new RDE document by clicking the "Enroll new 
document" button. This will generate a ticket that can be used to enroll the document using the API, and will display
a QR code that can be scanned by the RDE Client app to enroll the document. The ticket will expire when a new ticket is
created. In production, the ticket should be also have a max lifetime.

This process is not production ready. In production, the enrollment process should have more user interaction and
feedback.

## Privacy considerations
Right now the key server acts as a PGP-like public key register. This means that anyone can retrieve the public key of
any user as long as they know the email address of the user. It might be desirable to add some form of authentication
to the API, so that only authorized users or applications can access the register, and to add some form of rate limiting.
This is not a priority at the moment, but should be considered in the future.

## Security considerations
Within the RDE prototype, the purpose of the KeyServer is to provide a public key register for RDE keys and to link 
RDE enrollment parameters (think of them as public keys) to email addresses. The KeyServer is to be trusted for this 
binding. Other than that, the KeyServer does not have any special security requirements. It does not receive or process
any secret data within the RDE prototype.
