# Unit Tests

## Create a file for enviorment variables

First create a `.env` file here with

```ini
API_KEY=XXXXXXXX.XXXXXXXX.XXXXXXXXXXXXXXXXXXXXXXXX
API_BASE_URL=http://127.0.0.1:8000/v4
TIMEOUT=10
```

Use an API key with all permissions for testing

## Running the tests

To run one test, for example `test_archivo.py`, run:

```bash
python -m unittest tests.test_archivo
```

To run all tests, run:

```bash
python -m unittest discover tests
```
