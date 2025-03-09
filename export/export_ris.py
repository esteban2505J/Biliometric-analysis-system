from processing.format_converter import to_ris

def export_ris(data, filename="output.ris"):
    with open(filename, "w") as file:
        file.write(to_ris(data))

if __name__ == "__main__":
    sample_data = [{"title": "Sample Research", "authors": "John Doe"}]
    export_ris(sample_data)
