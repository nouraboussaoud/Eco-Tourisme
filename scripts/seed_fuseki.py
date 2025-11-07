"""
Seed Fuseki dataset with RDF files found in repository root.
Usage: python scripts\seed_fuseki.py
This script will POST `eco-toursime.rdf` to the Fuseki dataset `/tourisme-eco-2`.
Make sure Fuseki is running (start-all.bat) and that the dataset name matches.
"""
import os
import requests

ROOT = os.path.dirname(os.path.dirname(__file__))
RDF_PATH = os.path.join(ROOT, "eco-toursime.rdf")
FUSEKI_BASE = os.getenv("FUSEKI_ENDPOINT_BASE", "http://localhost:3030")
DATASET = os.getenv("FUSEKI_DATASET", "tourisme-eco-2")

UPLOAD_URL = f"{FUSEKI_BASE}/{DATASET}/data"


def seed_rdf(rdf_path: str, upload_url: str) -> None:
    if not os.path.exists(rdf_path):
        raise FileNotFoundError(f"RDF file not found: {rdf_path}")

    with open(rdf_path, "rb") as f:
        files = {"file": (os.path.basename(rdf_path), f, "application/rdf+xml")}
        print(f"Uploading {rdf_path} -> {upload_url}")
        resp = requests.post(upload_url, files=files)

    if resp.status_code in (200, 201, 204):
        print("Upload successful.")
    else:
        print(f"Upload failed: {resp.status_code}\n{resp.text}")
        resp.raise_for_status()


if __name__ == "__main__":
    try:
        seed_rdf(RDF_PATH, UPLOAD_URL)
    except Exception as e:
        print(f"Error during seeding: {e}")
        raise
