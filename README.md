# Web-Scraping-Campgrounds

This project is a Python-based application that aims to collect campground data across the United States through web scraping and store it in a database.

<pre> ## 📁 Project Structure ```bash case_study/ │ ├── src/ │ ├── scraper.py # Scraper functions │ ├── database.py # Database connection and helpers │ ├── __init__.py # Package initializer │ └── models/ │ ├── __init__.py # Models package initializer │ └── campground.py # Campground data model │ ├── main.py # Entry point for running the scraper ├── requirements.txt # Python dependencies ├── Dockerfile # Docker image definition ├── docker-compose.yml # Compose file for PostgreSQL ├── .env # Environment variables └── README.md # Project description ``` </pre>

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
