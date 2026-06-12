import pandas as pd

def extract_leads(csv_path: str):
    df = pd.read_csv(csv_path)

    results = []

    for _, row in df.iterrows():
        results.append({
            "name": row.get("name"),
            "phone": row.get("phone"),
            "address": row.get("address"),
            "url": row.get("url")
        })

    return results