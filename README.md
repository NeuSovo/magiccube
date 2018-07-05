# magiccube
[![Build Status](https://travis-ci.org/zxh326/magiccube.svg?branch=master)](https://travis-ci.org/zxh326/magiccube)
## Requirements
```bash
pythom -m venv venv
```
## Usage
* activate your venv
    * Windows

        ```.\venv\Scripts\activate```

    * Linux

        ```source venv/bin/activate```

    ```pip install -r requirements```

* run tests
```bash
pip install coverage
coverage run --source='.' --omit=venv/*,*/migrations/*,*_init__.py manage.py test
coverage report
```
* run server
* run celery
```bash
python manage.py celery worker -c 4 --loglevel=info
```
