# Web-Scraping-Campgrounds

This project is a Python-based application that aims to collect campground data across the United States through web scraping and store it in a database.

## Project Structure  
case_study/
├── src/
│   ├── scraper.py
│   ├── database.py
│   ├── __init__.py
│   └── models/
│       ├── __init__.py
│       └── campground.py
├── main.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
└── README.md

## Run Instructions
Install the required dependencies:
pip install -r requirements.txt

Start PostgreSQL using Docker:
docker-compose up -d

Run the scraper:
python main.py

### Example Output

Below is a sample output showing the first 5 campground records retrieved from the database:
example_output.PNG
