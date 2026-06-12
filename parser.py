import pandas as pd


def extract_leads(csv_path: str):
    df = pd.read_csv(csv_path)

    # keep only useful columns
    cols = ["name", "phone", "address", "url"]
    df = df[cols]

    # remove empty phones (CRITICAL for CRM use)
    df = df.dropna(subset=["phone"])

    # normalize strings
    df["phone"] = df["phone"].astype(str).str.strip()
    df["name"] = df["name"].astype(str).str.strip()

    # deduplicate by phone (most important improvement)
    df = df.drop_duplicates(subset=["phone"])

    # limit spam results
    df = df.head(15)

    return df.to_dict(orient="records")


def export_csv(leads, path="output/clean.csv"):
    df = pd.DataFrame(leads)
    df.to_csv(path, index=False)
    return path