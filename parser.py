import pandas as pd


def extract_leads(csv_path: str):
    df = pd.read_csv(csv_path)

    cols = ["name", "phone", "address", "url"]
    df = df[cols]

    # clean
    df = df.dropna(subset=["phone"])
    df["phone"] = df["phone"].astype(str).str.strip()

    # dedupe
    df = df.drop_duplicates(subset=["phone"])

    return df.head(15).to_dict(orient="records")


def export_csv(leads, path="output/clean.csv"):
    df = pd.DataFrame(leads)
    df.to_csv(path, index=False)
    return path