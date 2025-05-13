import requests
from time import sleep
from typing import List

from src.models.campground import Campground as CampgroundModel  # Pydantic model
from src.database import SessionLocal, Campground as CampgroundDB  # SQLAlchemy model

LAT_MIN, LAT_MAX = 24.396308, 49.384358
LON_MIN, LON_MAX = -125.0, -66.93457
STEP = 1.0  # 1 derece aralıkla böl

API_URL = "https://thedyrt.com/api/v6/locations/search-results"


def generate_bbox_list():
    bboxes = []
    lat = LAT_MIN
    while lat < LAT_MAX:
        lon = LON_MIN
        while lon < LON_MAX:
            bbox = [lon, lat, lon + STEP, lat + STEP]
            bboxes.append(bbox)
            lon += STEP
        lat += STEP
    return bboxes


def fetch_bbox_data(bbox) -> List[dict]:
    params = {
        "filter[search][bbox]": ",".join(map(str, bbox)),
        "page[number]": 1,
        "page[size]": 500,
        "sort": "recommended"
    }

    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])
    except requests.RequestException as e:
        print(f"[ERROR] API error for bbox {bbox}: {e}")
        return []


def process_campground(cg: dict):
    # attributes içeriğini düzleştiriyoruz
    flat = cg.get("attributes", {}).copy()
    flat["id"] = cg.get("id")
    flat["type"] = cg.get("type")
    flat["links"] = cg.get("links")

    required_fields = [
        "id", "type", "links", "name", "latitude", "longitude", "region-name",
        "accommodation-type-names"
    ]

    # Eksik alanları kontrol et
    missing = [f for f in required_fields if flat.get(f) is None]
    if missing:
        print(f"[WARNING] Skipping campground due to missing fields: {missing}")
        print(f"[DEBUG] Raw data: {cg}")
        return

    # API'den gelen veriyi logla
    print(f"[INFO] Processing campground: {flat['id']} - {flat.get('name', 'Unknown Name')}")

    # Pydantic ile doğrula
    try:
        validated = CampgroundModel.parse_obj(flat)
    except Exception as e:
        print(f"[ERROR] Pydantic validation failed: {e}")
        print(f"[DEBUG] Flat data: {flat}")
        return

    # Veritabanı işlemleri
    db = SessionLocal()
    db_obj = db.query(CampgroundDB).filter(CampgroundDB.id == validated.id).first()

    def join_list(l):
        return ",".join(l) if l else ""

    # Eğer veritabanında mevcutsa güncelle
    if db_obj:
        print(f"[INFO] Updating campground {validated.id}")
        db_obj.name = validated.name
        db_obj.region_name = validated.region_name
        db_obj.rating = validated.rating
        db_obj.reviews_count = validated.reviews_count
        db_obj.updated_at = validated.availability_updated_at
    else:
        print(f"[INFO] Inserting campground {validated.id}")
        db_obj = CampgroundDB(
            id=validated.id,
            type=validated.type,
            link_self=str(validated.links.self),
            name=validated.name,
            latitude=validated.latitude,
            longitude=validated.longitude,
            region_name=validated.region_name,
            administrative_area=validated.administrative_area,
            nearest_city_name=validated.nearest_city_name,
            accommodation_type_names=join_list(validated.accommodation_type_names),
            bookable=validated.bookable,
            camper_types=join_list(validated.camper_types),
            operator=validated.operator,
            photo_url=str(validated.photo_url) if validated.photo_url else None,
            photo_urls=join_list([str(url) for url in validated.photo_urls]),
            photos_count=validated.photos_count,
            rating=validated.rating,
            reviews_count=validated.reviews_count,
            slug=validated.slug,
            price_low=validated.price_low if validated.price_low is not None else 0.0,
            price_high=validated.price_high if validated.price_high is not None else 0.0,
            availability_updated_at=validated.availability_updated_at
        )
        db.add(db_obj)

    try:
        db.commit()
    except Exception as e:
        print(f"[ERROR] Failed to commit data: {e}")
        db.rollback()
    finally:
        db.close()


def run_scraper():
    bboxes = generate_bbox_list()
    for i, bbox in enumerate(bboxes):
        print(f"[INFO] Fetching bbox {i + 1}/{len(bboxes)}: {bbox}")
        results = fetch_bbox_data(bbox)
        print(f"[INFO] Found {len(results)} campgrounds")
        for cg in results:
            process_campground(cg)
        sleep(1)  # API'yı çok zorlamamak için bekleme


if __name__ == "__main__":
    run_scraper()










