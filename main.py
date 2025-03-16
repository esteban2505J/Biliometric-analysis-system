import subprocess
import threading
import sys

# Paths to your scraper scripts
scraper1 = r"C:\Users\newUs\Documents\uni\projects\bibliometricProject\scrapers\IEE_screper.py"
scraper2 = r"C:\Users\newUs\Documents\uni\projects\bibliometricProject\scrapers\sage_scraper.py"
scraper3 = r"C:\Users\newUs\Documents\uni\projects\bibliometricProject\scrapers\science_direct_scraper.py"

# Path to your processing script
processing_script = r"C:\Users\newUs\Documents\uni\projects\bibliometricProject\processing\unifyBibtext.py"

def run_scraper(script):
    """Runs a scraper script using the Python interpreter from the virtual environment."""
    subprocess.run([sys.executable, script], check=True)

# Run all scrapers concurrently using threads
threads = [
    threading.Thread(target=run_scraper, args=(scraper1,)),
    threading.Thread(target=run_scraper, args=(scraper2,)),
    threading.Thread(target=run_scraper, args=(scraper3,))
]

# Start all scrapers
for thread in threads:
    thread.start()

# Wait until all scrapers finish
for thread in threads:
    thread.join()

print("✅ All scrapers finished. Starting processing...")

# Run the processing script after scrapers complete
subprocess.run([sys.executable, processing_script], check=True)

print("✅ Processing complete!")
