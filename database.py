from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Docker environment'tan DB bağlantısı alıyoruz
DATABASE_URL = os.getenv("DB_URL", "postgresql://user:password@localhost:5432/case_study")


# Engine ve Session tanımlıyoruz
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tüm modellerin türeyeceği Base sınıfı
Base = declarative_base()

class Campground(Base):
    __tablename__ = "campground"

    id = Column(String, primary_key=True, index=True)
    type = Column(String)
    link_self = Column(String)  # From CampgroundLinks.self
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    region_name = Column(String)
    administrative_area = Column(String)
    nearest_city_name = Column(String)
    accommodation_type_names = Column(String)  # Join list with comma
    bookable = Column(Boolean, default=False)
    camper_types = Column(String)  # Join list with comma
    operator = Column(String)
    photo_url = Column(String)
    photo_urls = Column(String)  # Join list with comma
    photos_count = Column(Integer, default=0)
    rating = Column(Float)
    reviews_count = Column(Integer, default=0)
    slug = Column(String)
    price_low = Column(Float)
    price_high = Column(Float)
    availability_updated_at = Column(DateTime)


# ✅ Tabloları oluşturmak için:
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("✅ Campground tablosu başarıyla oluşturuldu.")
