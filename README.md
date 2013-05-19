# Vital Stats Manager - Server

## Getting Started
1. Clone the repo:
`git clone https://github.com/jcgharvey/vsm-svr.git/`

2. Create a virtualenv inside the project folder (vsm-svr):
`virtualenv venv`

3. Activate virtualenv:
`source venv/bin/activate` (Linux)

4. Install dependencies:
`pip install -r requirements.txt`

5. Run `python` in shell and then:
```python
>>> import models
>>> models.init_db([num_patients [, min_vital_infos [, max_vital_infos]]]):
```

6. Run the app:
`python app.py`
