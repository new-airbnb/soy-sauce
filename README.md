# soy-sauce

[![Build Status](https://travis-ci.com/new-airbnb/soy-sauce.svg?branch=master)](https://travis-ci.com/new-airbnb/soy-sauce) [![Coverage Status](https://coveralls.io/repos/github/new-airbnb/soy-sauce/badge.svg?branch=master)](https://coveralls.io/github/new-airbnb/soy-sauce?branch=master) ![GitHub issues](https://img.shields.io/github/issues/new-airbnb/soy-sauce.svg) ![GitHub closed issues](https://img.shields.io/github/issues-closed-raw/new-airbnb/soy-sauce.svg) ![GitHub pull requests](https://img.shields.io/github/issues-pr/new-airbnb/soy-sauce.svg) ![GitHub last commit](https://img.shields.io/github/last-commit/new-airbnb/soy-sauce.svg) ![GitHub commit activity](https://img.shields.io/github/commit-activity/m/new-airbnb/soy-sauce.svg)

Hey there, welcome to our repository of backend, find the wiki here: [wiki](https://github.com/new-airbnb/wiki)

### Deployment

To start with this project, firstly you need to edit `config.json`

```
{
    "log_level": "ERROR",
    "database_name": "your database name",
    "database_uri": "your database uri" 
    "sentry_dsn": "your sentry dsn",
    "house_location_collection": "the name of collection to store geo inforamtion",
    "test_database_name": "your test database name",
    "test_database_uri": "your test database uri"
}
```

Then, try this command to run the server

```
python manage.py runserver 0.0.0.0:8000
```

In the end, visit ```http://127.0.0.1:8000``` to see the welcome page
