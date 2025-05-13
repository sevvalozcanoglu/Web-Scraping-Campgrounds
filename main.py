"""
Main entrypoint for The Dyrt web scraper case study.

Usage:
    The scraper can be run directly (`python main.py`) or via Docker Compose (`docker compose up`).

If you have any questions in mind you can connect to me directly via info@smart-maple.com
"""


from src.scraper import run_scraper  # Burada scraper fonksiyonunu içe aktarıyoruz

if __name__ == "__main__":
    print("Starting the scraper...")
    run_scraper()  # Scraper'ı başlatıyoruz



