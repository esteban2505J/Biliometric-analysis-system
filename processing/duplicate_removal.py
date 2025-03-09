def remove_duplicates(data):
    seen_titles = set()
    unique_data = []
    
    for record in data:
        if record["title"] not in seen_titles:
            seen_titles.add(record["title"])
            unique_data.append(record)
    
    return unique_data
