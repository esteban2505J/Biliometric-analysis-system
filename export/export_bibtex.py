from processing.format_converter import to_bibtex

def export_bibtex(data, filename="output.bib"):
    with open(filename, "w") as file:
        file.write(to_bibtex(data))

if __name__ == "__main__":
    sample_data = [{"title": "Sample Research", "authors": "John Doe"}]
    export_bibtex(sample_data)
