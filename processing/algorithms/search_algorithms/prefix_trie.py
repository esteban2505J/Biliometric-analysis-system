import re  # For text cleaning
import bibtexparser
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))  # Agrega el directorio actual al path

from Trie import Trie

def count_words_abstracts(file_path):
    # Load the BibTeX file
    with open(file_path, encoding="utf-8") as bib_file:
        bib_database = bibtexparser.load(bib_file)

    # Extract abstracts and store them in a list
    abstracts = [entry["abstract"] for entry in bib_database.entries if "abstract" in entry]

    # Create a Trie instance
    trie = Trie()

    # Insert words from abstracts into the Trie
    for abstract in abstracts:
        words = re.findall(r"\b\w+\b", abstract.lower())  # Tokenize words (convert to lowercase)
        for word in words:
            trie.insert(word)

    # Example: Count occurrences of specific words
    search_words = ["abstraction", "motivation", "algorithm", "persistence",
                    "coding", "block", "creativity", "mobile", "application",
                    "logic", "programming", "conditionals", "robotic", "loops", "scratch"]

    # Store results in a single dictionary
    results = {}

    for word in search_words:
        count = trie.count_occurrences(word)  # Get count
        # print(f"'{word}' appears {count} times")
        results[word] = count  # Correct way to store key-value pairs in a dictionary

    # print(results)  # Debugging output
    return results  # Returns a single dictionary

if __name__ == "__main__":
    file_path = r"C:\Users\newUs\Documents\uni\projects\bibliometricProject\output\unified_cleaned.bib"
    
    count_words_abstracts(file_path)
