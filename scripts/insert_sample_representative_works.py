import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from sqlmodel import Session
from app.database import engine
from app.models import RepresentativeWork


def insert_sample_data():
    sample_works = [
        {
            "title": "Scalable manufacturing breakthrough",
            "description": "High-index atomic layer-polymer hybrid metasurfaces for metaphotonics",
            "image_path": "/static/uploads/sample1.jpg",
            "citation": "Nature Materials 22, 474-481 (2023)",
            "order_index": 1,
            "is_active": True
        },
        {
            "title": "Next-generation displays",
            "description": "Single-layer waveguide display for full-colour augmented reality",
            "image_path": "/static/uploads/sample2.jpg",
            "citation": "Nature Nanotechnology 20, 747-754 (2025)",
            "order_index": 2,
            "is_active": True
        },
        # 더 많은 샘플 데이터...
    ]

    db = Session(engine)
    try:
        for work_data in sample_works:
            work = RepresentativeWork(**work_data)
            db.add(work)
        db.commit()
        print("✅ Sample representative works inserted successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    insert_sample_data()
