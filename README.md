# Text Checksum

A small FastAPI app that displays a welcome page and generates SHA-256 checksums
for submitted text.

## Setup

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run

Start the development server from the project directory:

```bash
uvicorn main:app --reload
```

Open [http://localhost:8000](http://localhost:8000) to use the form. The
interactive API documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs).

## API

Both `POST /generate` and `POST /checksum` accept JSON containing a `text`
string and return its SHA-256 hex digest:

```json
{"text": "hello"}
```

Example response:

```json
{"checksum": "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"}
```

## Tests

Run the test suite with:

```bash
pytest -v
```
