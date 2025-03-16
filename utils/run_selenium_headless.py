import sys
import os
import subprocess
import threading
import tempfile
import shutil
import re

def modify_script_for_headless(original_script_path):
    """
    Creates a temporary copy of the script and modifies it to run in headless mode.
    Returns the path to the modified script.
    """
    # Create a temporary file
    temp_dir = tempfile.gettempdir()
    script_name = os.path.basename(original_script_path)
    modified_script_path = os.path.join(temp_dir, f"headless_{script_name}")
    
    # Read the original script
    with open(original_script_path, 'r', encoding='utf-8') as file:
        script_content = file.read()
    
    # Check if the script already has headless options
    if "--headless" in script_content:
        print(f"Script {script_name} already has headless options.")
        return original_script_path
    
    # Add headless options to the script
    headless_code = """
# Added headless options
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
"""
    
    # Replace webdriver.Chrome() with webdriver.Chrome(options=chrome_options)
    modified_content = re.sub(
        r'webdriver\.Chrome\((.*?)\)',
        lambda m: f'webdriver.Chrome(options=chrome_options, {m.group(1)})' if m.group(1) else 'webdriver.Chrome(options=chrome_options)',
        script_content
    )
    
    # Add the headless options code after the import section
    import_section_end = 0
    for match in re.finditer(r'^import |^from ', modified_content, re.MULTILINE):
        line_end = modified_content.find('\n', match.start())
        if line_end > import_section_end:
            import_section_end = line_end
    
    final_content = (
        modified_content[:import_section_end + 1] + 
        headless_code + 
        modified_content[import_section_end + 1:]
    )
    
    # Write the modified script to the temporary file
    with open(modified_script_path, 'w', encoding='utf-8') as file:
        file.write(final_content)
    
    print(f"Created headless version of {script_name} at {modified_script_path}")
    return modified_script_path

def run_script(script_path, is_modified=False):
    """Run a Python script using subprocess."""
    try:
        script_name = os.path.basename(script_path)
        print(f"Starting script: {script_name}")
        
        subprocess.run([sys.executable, script_path], check=True)
        
        print(f"Finished script: {script_name}")
        
        # Clean up the temporary file if it was modified
        if is_modified and os.path.exists(script_path) and script_path.startswith(tempfile.gettempdir()):
            os.remove(script_path)
            print(f"Removed temporary script: {script_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")
    except Exception as e:
        print(f"Unexpected error with {script_name}: {e}")

def main():
    # List of script paths - replace with your actual script paths
    original_script_paths = [
        "C:\Users\newUs\Documents\uni\projects\bibliometricProject\scrapers\science_direct_scraper.py",
        "path/to/your/second_script.py",
        "path/to/your/third_script.py"
    ]
    
    # Create a thread for each script
    threads = []
    for script_path in original_script_paths:
        # Modify the script to run in headless mode
        modified_path = modify_script_for_headless(script_path)
        
        # Determine if the script was modified
        is_modified = modified_path != script_path
        
        # Create and start a thread to run the script
        thread = threading.Thread(target=run_script, args=(modified_path, is_modified))
        threads.append(thread)
    
    # Start all threads
    for thread in threads:
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    print("All scripts have completed!")

if __name__ == "__main__":
    main()