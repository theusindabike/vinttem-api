# vintem_api
- Python 3.10.6

## Install
```console
git clone git@github.com:theusindabike/vintem_api.git
cd vintem_api
python -m venv .vintem_api
source .vintem_api/bin/activate
pip install -r requirements-dev.txt
cp contrib/env-sample .env
python manage.py test 
```

## Deploy

```console
heroku create newinstance
heroku config:push
heroku config:set SECRET_KEY=`python contrib/secret_gen.py`
heroku confit:set DEBUG=False
#config email
git push heroku master
```
