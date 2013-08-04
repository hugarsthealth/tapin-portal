# Tap In Portal

## Development
1. Clone the repo:
`git clone https://github.com/hugarsthealth/tapin-portal.git/`

2. Create a virtualenv inside the project folder (tapin-portal):
`virtualenv venv`

3. Activate virtualenv:
`source venv/bin/activate` (Linux)

4. Install dependencies:
`pip install -r requirements.txt`

5. Run `python` in shell and then:
```python
>>> import models
>>> models.init_db([num_patients [, min_checkins [, max_checkins]]]):
```

6. Run the app:
`python app.py`

## Production
In addition to the above instructions, to run the application in production
requires two environment variables to be set:

1. `DATABASE_URL: <db connection string>` where db connection string is something
like `postgres://user:password@host:port/database` (most databases are supported).
If this environment variable is not set, the application will try to use a local
SQLite database (as in development).

2. `PRODUCTION: True` in order to disable debug mode in Flask.
