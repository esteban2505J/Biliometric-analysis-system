def to_bibtex(data):
    bibtex = ""
    for record in data:
        bibtex += f"@article{{\n  title={{ {record['title']} }},\n  author={{ {record['authors']} }}\n}}\n\n"
    return bibtex

def to_ris(data):
    ris = ""
    for record in data:
        ris += f"TY  - JOUR\nTI  - {record['title']}\nAU  - {record['authors']}\nER  - \n\n"
    return ris
