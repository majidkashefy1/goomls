import pandas as pd


def extract_leads(csv_path: str):
    df = pd.read_csv(csv_path)

    # normalize column names
    df.columns = [c.strip().lower() for c in df.columns]

    # DEBUG (VERY IMPORTANT FIRST TIME)
    print("CSV columns:", df.columns.tolist())

    # flexible mapping (handles scraper variations)
    name_col = next((c for c in df.columns if c in ["name", "title", "business_name"]), None)
    phone_col = next((c for c in df.columns if "phone" in c), None)
    address_col = next((c for c in df.columns if "address" in c or "full_address" in c), None)
    url_col = next((c for c in df.columns if c in ["url", "link", "website"]), None)

    if not phone_col:
        return []

    result = []

    for _, row in df.iterrows():
        result.append({
            "name": row[name_col] if name_col else None,
            "phone": row[phone_col],
            "address": row[address_col] if address_col else None,
            "url": row[url_col] if url_col else None,
        })

    # clean
    clean = []
    seen = set()

    for r in result:
        phone = str(r["phone"]).strip()

        if phone == "nan" or phone in seen:
            continue

        seen.add(phone)
        clean.append(r)

    return clean[:15]


def export_csv(leads, path="output/clean.csv"):
    df = pd.DataFrame(leads)
    df.to_csv(path, index=False)
    return path