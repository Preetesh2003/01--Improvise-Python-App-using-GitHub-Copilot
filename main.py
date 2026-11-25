"""A small FastAPI app that generates SHA-256 checksums for text."""

import hashlib

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

PARTICIPANT_NAME = "Preetesh Singha"

app = FastAPI(title="Text Checksum")


class Text(BaseModel):
    """Text submitted to the checksum endpoints."""

    text: str


def _checksum(text: str) -> str:
    """Return the SHA-256 hex digest for UTF-8 encoded text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@app.get("/", response_class=HTMLResponse)
async def home() -> str:
    """Show a welcome message and a form for generating a checksum."""
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Text Checksum</title>
  </head>
  <body>
    <h1>Welcome, {PARTICIPANT_NAME}!</h1>
    <form id="checksum-form">
      <label for="text">Text</label>
      <input id="text" name="text" type="text" required>
      <button type="submit">Generate checksum</button>
    </form>
    <p id="result" aria-live="polite"></p>
    <script>
      document.getElementById("checksum-form").addEventListener("submit", async (event) => {{
        event.preventDefault();
        const text = document.getElementById("text").value;
        const response = await fetch("/generate", {{
          method: "POST",
          headers: {{ "Content-Type": "application/json" }},
          body: JSON.stringify({{ text }})
        }});
        const result = await response.json();
        document.getElementById("result").textContent =
          response.ok ? `SHA-256: ${{result.checksum}}` : "Unable to generate checksum.";
      }});
    </script>
  </body>
</html>"""


@app.post("/generate")
async def generate_checksum(payload: Text) -> dict[str, str]:
    """Generate a checksum for text submitted by the web form."""
    return {"checksum": _checksum(payload.text)}


@app.post("/checksum")
async def checksum(payload: Text) -> dict[str, str]:
    """Return the SHA-256 checksum for submitted text."""
    return {"checksum": _checksum(payload.text)}
