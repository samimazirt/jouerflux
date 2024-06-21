JouerFlux

To test:

in the app/ folder run:

'python -m venv venv'

then 

'source venv/scripts/activate'

then 

'pip install -r requirements.txt'

then 

'flask run' and open localhost:5000

OR Docker:

docker build -t jouerflux .
docker run -p 5000:5000 jouerflux

#TODO

check if firewalls/policies/rules already exists before creating
unit tests
test traffic simulation ??
add firewalls type (forti/checkpoint/palo) ?
get closer to real firewalls...