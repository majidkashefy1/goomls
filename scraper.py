import os
import subprocess

OUTPUT_DIR = "output"
QUERY_FILE = "queries.txt"

def run_scraper(query: str):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # write query to file
    with open(QUERY_FILE, "w", encoding="utf-8") as f:
        f.write(query)

    cmd = [
        "docker", "run", "--rm",
        "-v", "gmaps-cache:/opt",
        "-v", f"{os.getcwd()}/{QUERY_FILE}:/queries.txt:ro",
        "-v", f"{os.getcwd()}/{OUTPUT_DIR}:/out",
        "gosom/google-maps-scraper",
        "-input", "/queries.txt",
        "-results", "/out/results.csv",
        "-depth", "1",
        "-exit-on-inactivity", "2m"
    ]

    subprocess.run(cmd, check=True)

    return f"{OUTPUT_DIR}/results.csv"