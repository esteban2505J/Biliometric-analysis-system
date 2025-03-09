import re

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def clean_data(data):
    for record in data:
        record["title"] = clean_text(record["title"])
        record["authors"] = clean_text(record.get("authors", "Unknown"))
    return data
