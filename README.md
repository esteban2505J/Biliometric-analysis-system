# Bibliometric Data Scraper

## 📌 Project Overview
This project is a **bibliometric data analyst** that collects, processes, and structures information from various academic sources. It extracts bibliographic data (titles, authors, journals, years, etc.) using web scraping, then formats it into structured outputs like **BibTeX** for academic use.

Additionally, the collected data is **unified from multiple datasets**, sorted using **sorting algorithms**, and the performance of these algorithms is **analyzed and visualized through plots**.

## 🚀 Features
- **Web Scraping**: Extracts article information from academic databases.
- **JavaScript Handling**: Uses Selenium for dynamic content scraping.
- **Data Cleaning**: Standardizes and removes duplicates using Pandas.
- **Sorting & Performance Analysis**: Orders data using sorting algorithms and visualizes their efficiency.
- **Export Formats**: Saves data in **RIS** and **BibTeX** formats for citation management.
- **Logging & Error Handling**: Implements logging mechanisms to track scraping status.

## 🛠️ Technologies Used
- **Python 3.13.2**
- `selenium` – Handling JavaScript-loaded pages
- `pandas` – Cleaning and processing data
- `numpy` – Efficient numerical operations
- `bibtexparser` & `rispy` – Exporting data in academic formats
- `dotenv` – Managing environment variables
- `matplotlib` – Plotting sorting algorithm performance.

## 📥 Installation
1. **Clone the Repository**
   ```sh
   git clone https://github.com/esteban2505J/Bibliometric-analysis-system.git
   cd Bibliometric-analysis-system
   ```

2. **Create a Virtual Environment** (Optional but recommended)
   ```sh
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate    # On Windows
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

## 🔧 Usage
1. **Run the Scraper**
   ```sh
   python main.py
   ```

2. **Configure Environment Variables**
   - Create an `.env` file and add the “EMAIL” and “PASSWORD” credentials used in science direct (you need an academic account).

3. **Output Files**
   - Data is saved in the `output/` directory in **BibTeX** format.


## 📄 License
This project is licensed under the MIT License.

