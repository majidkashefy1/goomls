import os
import subprocess
import time

OUTPUT_DIR = "output"
QUERY_FILE = "queries.txt"


def run_scraper(query: str):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # write query
    with open(QUERY_FILE, "w", encoding="utf-8") as f:
        f.write(query)

    csv_path = f"{OUTPUT_DIR}/results.csv"

    cmd = [
        "docker", "run", "--rm",
        "-v", "gmaps-cache:/opt",
        "-v", f"{os.getcwd()}/{QUERY_FILE}:/queries.txt:ro",
        "-v", f"{os.getcwd()}/{OUTPUT_DIR}:/out",
        "gosom/google-maps-scraper",
        "-input", "/queries.txt",
        "-results", "/out/results.csv",
        "-depth", "2",
        "-exit-on-inactivity", "90s"
    ]

    start = time.time()
    subprocess.run(cmd, check=True)
    print(f"Scraping finished in {time.time() - start:.2f}s")

    return csv_path