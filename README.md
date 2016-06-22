[![Build Status](https://travis-ci.org/andela-mnzomo/flask-bucketlist-api.svg?branch=develop)](https://travis-ci.org/andela-mnzomo/flask-bucketlist-api)
[![Coverage Status](https://coveralls.io/repos/github/andela-mnzomo/flask-bucketlist-api/badge.svg?branch=develop)](https://coveralls.io/github/andela-mnzomo/flask-bucketlist-api?branch=develop)
[![Code Health](https://landscape.io/github/andela-mnzomo/flask-bucketlist-api/develop/landscape.svg?style=flat)](https://landscape.io/github/andela-mnzomo/flask-bucketlist-api/develop)
![alt text](https://img.shields.io/badge/python-2.7-blue.svg)
[![DUB](https://img.shields.io/dub/l/vibe-d.svg)]()

# Flask Bucket List API
According to the [Oxford Dictionary](http://www.oxforddictionaries.com/definition/english/bucket-list),
a *bucket list* is a *number of experiences or achievements that a person hopes
to have or accomplish during their lifetime*.

This is a RESTful API for an online Bucket List service using `Flask`.

## Installation and Set Up
Clone the repo from GitHub:
```
git clone https://github.com/andela-mnzomo/flask-bucketlist-api
```

Fetch from the develop branch:
```
git fetch origin develop
```

Navigate to the root folder:
```
cd flask-bucketlist-api
```

Install the required packages:
```
pip install -r requirements.txt
```

Initialize, migrate, and upgrade the database:
```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

## Launching the Program
Run ```python run.py```. You may use [Postman](https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?hl=en) for Google Chrome to run the API.

## API Endpoints

| Resource URL | Methods | Description | Requires Token |
| -------- | ------------- | --------- |--------------- |
| `/api/v1/` | GET  | The index | FALSE |
| `/api/v1/auth/register/` | POST  | User registration | FALSE |
|  `/api/v1/auth/login/` | POST | User login | FALSE |
| `/api/v1/bucketlists/` | GET, POST | A user's bucket lists | TRUE |
| `/api/v1/bucketlists/<id>/` | GET, PUT, DELETE | A single bucket list | TRUE |
| `/api/v1/bucketlists/<id>/items/` | GET, POST | Items in a bucket list | TRUE |
| `/api/v1/bucketlists/<id>/items/<item_id>/` | GET, PUT, DELETE| A single bucket list item | TRUE |

| Method | Description |
|------- | ----------- |
| GET | Retrieves a resource(s) |
| POST | Creates a new resource |
| PUT | Updates an existing resource |
| DELETE | Deletes an existing resource |

## Sample Requests

To register a new user:
![User Registration](https://github.com/andela-mnzomo/flask-bucketlist-api/blob/develop/app/screenshots/register.png)

To log the user in:
![User Login](https://github.com/andela-mnzomo/flask-bucketlist-api/blob/develop/app/screenshots/login.png)

To add a new bucket list (includes the token in the header):
![Adding Bucket List](https://github.com/andela-mnzomo/flask-bucketlist-api/blob/develop/app/screenshots/add_bucketlist.png)

## Testing
To test, run the following command: ```nosetests```

## Built With...
* [Flask](http://flask.pocoo.org/)
* [Flask-RESTful](http://flask-restful-cn.readthedocs.io/en/0.3.4/)
* [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.1/)

## Credits

[Mbithe Nzomo](https://github.com/andela-mnzomo)
