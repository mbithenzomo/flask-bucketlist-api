![alt text](https://img.shields.io/badge/python-2.7-blue.svg)
[![DUB](https://img.shields.io/dub/l/vibe-d.svg)]()
[![Coverage Status](https://coveralls.io/repos/github/andela-mnzomo/flask-bucketlist-api/badge.svg?branch=develop)](https://coveralls.io/github/andela-mnzomo/flask-bucketlist-api?branch=develop)

# Flask Bucket List API
According to the [Oxford Dictionary](http://www.oxforddictionaries.com/definition/english/bucket-list),
a *bucket list* is a *number of experiences or achievements that a person hopes
to have or accomplish during their lifetime*.

This is an API for an online Bucket List service using `Flask`.

## Installation
Clone the repo from GitHub:
```
git clone https://github.com/andela-mnzomo/flask-bucketlist-api
```

Fetch from the features-review branch:
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

## Launching the Program
Run ```python run.py```

## API Resources

| Resource URL | Methods | Description |
| -------- | ------------- | --------- |
| `/api/v1.0/` | GET  | The index |
| `/api/v1.0/auth/register/` | POST  | User registration |
|  `/api/v1.0/auth/login/` | POST | User login|
| `/api/v1.0/bucketlists/` | GET, POST | A user's bucket lists |
| `/api/v1.0/bucketlists/<id>/` | GET, PUT, DELETE | A single bucket list |
| `/api/v1.0/bucketlists/<id>/items/` | GET, POST | Items in a bucket list |
| GET `/api/v1.0/bucketlists/<id>/items/<item_id>/` | GET, PUT, DELETE| A single bucket list item|

| Method | Description |
|------- | ----------- |
| GET | Retrieves a resource(s) |
| POST | Creates a new resource |
| PUT | Updates an existing resource |
| DELETE | Deletes an existing resource |

## Testing
To test, run the following command: ```nosetests```

## Credits

[Mbithe Nzomo](https://github.com/andela-mnzomo)
