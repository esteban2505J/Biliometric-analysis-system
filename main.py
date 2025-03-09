
from scrapers.selenium_scraper import scrape_dynamic_site
from processing.data_cleaning import clean_data
from processing.duplicate_removal import remove_duplicates
from export.export_bibtex import export_bibtex
from export.export_ris import export_ris

def main():
    
    selenium_data = scrape_dynamic_site("https://example.com/js-research")

    # 2. Combine & Clean data
    all_data =  selenium_data
    cleaned_data = clean_data(all_data)

    # 3. Remove duplicates
    unique_data = remove_duplicates(cleaned_data)

    # 4. Export data
    export_bibtex(unique_data, "bibliography.bib")
    export_ris(unique_data, "bibliography.ris")

if __name__ == "__main__":
    main()
