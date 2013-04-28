vsm-svr
=======

## Getting Started
1. Clone the repo
`git clone https://github.com/jcgharvey/vsm-svr.git/`

2. Create a virtualenv
`virtualenv venv`

3. Activate virtualenv
`source venv/bin/activate` (Linux)

4. Install dependencies
`pip install -r requirements.txt`

5. Generate sample data
```
$ python
>>> from models import sampledata
>>> sampledata.main()

```

6. Run the app
`python app.py`
