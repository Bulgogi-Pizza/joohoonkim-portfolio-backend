import os
import sys

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from sqlmodel import Session

from app.database import engine, create_db_and_tables, test_db_connection, \
    SessionLocal
from app.models import Education, Experience, Award, Publication, Conference


def get_db_session():
    """데이터베이스 세션을 생성합니다."""
    return Session(engine)


def insert_education_data(db: Session):
    education_data = [
        {
            "degree": "M.S./Ph.D. Candidate in Mechanical Engineering",
            "institution": "Pohang University of Science and Technology",
            "location": "Korea",
            "start_year": "2021",
            "end_year": "Current",
            "advisor": "Prof. Junsuk Rho"
        },
        {
            "degree": "B.S. in Mechanical Engineering",
            "institution": "Pohang University of Science and Technology",
            "location": "Korea",
            "start_year": "2017",
            "end_year": "2021",
            "advisor": "Prof. Wonkyu Moon"
        }
    ]

    for edu in education_data:
        db_education = Education(**edu)
        db.add(db_education)

    db.commit()
    print("Education data inserted successfully!")


def insert_experience_data(db: Session):
    experience_data = [
        {
            "position": "Entrepreneurial Member",
            "organization": "Metacloud",
            "location": "Korea",
            "start_year": "2023",
            "end_year": "2024",
            "description": "Funded by I-Corps program (Startup investment program by the Ministry of Science and ICT)"
        },
        {
            "position": "Visiting Researcher",
            "organization": "Plant and Food Research",
            "location": "New Zealand",
            "start_year": "2023",
            "end_year": "2023",
            "host_advisor": "Dr. Jonghyun Choi"
        },
        {
            "position": "Visiting Researcher",
            "organization": "Northeastern University",
            "location": "USA",
            "start_year": "2022",
            "end_year": "2022",
            "host_advisor": "Prof. Yongmin Liu"
        },
        {
            "position": "Visiting Researcher",
            "organization": "Massachusetts Institute of Technology (MIT)",
            "location": "USA",
            "start_year": "2022",
            "end_year": "2022",
            "host_advisor": "Prof. Juejun Hu"
        },
        {
            "position": "Entrepreneurial Leader",
            "organization": "ThinLens",
            "location": "Korea",
            "start_year": "2022",
            "end_year": "2023",
            "description": "Funded by I-Corps program (Startup investment program by the Ministry of Science and ICT)"
        },
        {
            "position": "Undergraduate Researcher",
            "organization": "Nanoscale photonics & integrated manufacturing lab, Pohang University of Science and Technology",
            "location": "Korea",
            "start_year": "2019",
            "end_year": "2021",
            "host_advisor": "Prof. Junsuk Rho"
        },
        {
            "position": "Internship",
            "organization": "Video Display (VD) Division, Samsung Electronics",
            "location": "Korea",
            "start_year": "2018",
            "end_year": "2018"
        }
    ]

    for exp in experience_data:
        db_experience = Experience(**exp)
        db.add(db_experience)

    db.commit()
    print("Experience data inserted successfully!")


def insert_awards_data(db: Session):
    awards_data = [
        {"title": "BK21 Four Excellence Award", "organization": "POSTECH",
         "location": "Korea", "year": "2025", "rank": "1st place"},
        {"title": "BK21+ Best Paper Award", "organization": "POSTECH",
         "location": "Korea", "year": "2024", "rank": "1st place"},
        {"title": "Editage grant", "organization": "Editage",
         "location": "Korea", "year": "2024", "rank": "2nd place"},
        {"title": "Best Poster Awards",
         "organization": "the 24th International Meeting on Information Display (IMID)",
         "location": "Korea", "year": "2024"},
        {"title": "POSTECH Alchemist Fellowship", "organization": "POSTECH",
         "location": "Korea", "year": "2024"},
        {"title": "Presidential Science Fellowship (Ph.D.)",
         "organization": "the Ministry of Science and ICT", "location": "Korea",
         "year": "2024"},
        {"title": "Asan Biomedical Science Fellowship",
         "organization": "the Asan Foundation", "location": "Korea",
         "year": "2024"},
        {"title": "iCore Lab Start-Up Award",
         "organization": "the Ministry of Science and ICT", "location": "Korea",
         "year": "2024", "rank": "Grand Prize"},
        {"title": "BK21 Four Excellence Award", "organization": "POSTECH",
         "location": "Korea", "year": "2024", "rank": "1st place"},
        {"title": "NAEK Wonik \"Young Engineers Honor Society\" Award",
         "organization": "National Academy of Engineering of Korea (NAEK)",
         "location": "Korea", "year": "2024", "rank": "1st place"},
        {"title": "BK21+ Best Paper Award",
         "organization": "Department of Mechanical Engineering, POSTECH",
         "location": "Korea", "year": "2023", "rank": "1st place"},
        {"title": "Monthly Editor's Pick Reviewer in July",
         "organization": "Light: Science & Applications (LSA)",
         "location": "USA", "year": "2023"},
        {"title": "3·1 Fellowship",
         "organization": "the Samil (3·1) Cultural Foundation",
         "location": "Korea", "year": "2023"},
        {"title": "KIDS Award",
         "organization": "the 23th International Meeting on Information Display (IMID)",
         "location": "Korea", "year": "2023", "rank": "Gold, 1st place"},
        {"title": "POSTECH Alchemist Fellowship", "organization": "POSTECH",
         "location": "Korea", "year": "2023"},
        {"title": "Link Award",
         "organization": "Samsung Global Technology Symposium (GTS)",
         "location": "Korea", "year": "2023"},
        {"title": "BK21 Four Excellence Award", "organization": "POSTECH",
         "location": "Korea", "year": "2023", "rank": "2nd place"},
        {"title": "Postechian's Choice Award", "organization": "POSTECH",
         "location": "Korea", "year": "2023"},
        {"title": "Silver Prize",
         "organization": "the 29th Samsung Humantech Paper Award",
         "location": "Korea", "year": "2023", "rank": "2nd place"},
        {"title": "Talent Award of Korea",
         "organization": "the Ministry of Education of the Korean Government",
         "location": "Korea", "year": "2022"},
        {"title": "Iksung Memorial Award", "organization": "POSTECH",
         "location": "Korea", "year": "2022"},
        {"title": "BK21+ Best Paper Award", "organization": "POSTECH",
         "location": "Korea", "year": "2022", "rank": "2nd place"},
        {"title": "KIDS Award",
         "organization": "the 22nd International Meeting on Information Display (IMID)",
         "location": "Korea", "year": "2022", "rank": "Gold, 1st place"},
        {"title": "POSTECH Alchemist Fellowship", "organization": "POSTECH",
         "location": "Korea", "year": "2022"},
        {"title": "BK21 Four Excellence Award", "organization": "POSTECH",
         "location": "Korea", "year": "2021", "rank": "2nd place"},
        {"title": "Best Poster Award",
         "organization": "the 21st International Meeting on Information Display (IMID)",
         "location": "Korea", "year": "2021"},
        {"title": "POSTECH Alchemist Fellowship", "organization": "POSTECH",
         "location": "Korea", "year": "2021"},
        {"title": "Best Paper Award",
         "organization": "the Korean Society of Mechanical Engineers (KSME) Spring Meeting",
         "location": "Korea", "year": "2021"}
    ]

    for award in awards_data:
        db_award = Award(**award)
        db.add(db_award)

    db.commit()
    print("Awards data inserted successfully!")


def insert_publications_data(db: Session):
    publications_data = [
        {
            "title": "Scalable manufacturing of high-index atomic layer-polymer hybrid metasurfaces for metaphotonics in the visible",
            "authors": "J. Kim et al.",
            "journal": "Nature Materials",
            "year": "2023",
            "impact_factor": 38.5,
            "volume": "22",
            "pages": "474-481",
            "is_first_author": True
        },
        {
            "title": "Roll-to-plate printable RGB achromatic metalens for wide-field-of-view holographic near-eye display",
            "authors": "J. Kim et al.",
            "journal": "Nature Materials",
            "year": "2025",
            "impact_factor": 38.5,
            "volume": "24",
            "pages": "535-543",
            "is_first_author": True
        },
        {
            "title": "Full-color augmented reality near-eye displays using single-layer achromatic metasurface waveguides",
            "authors": "J. Kim et al.",
            "journal": "Nature Nanotechnology",
            "year": "2025",
            "impact_factor": 34.9,
            "volume": "20",
            "pages": "747-754",
            "is_first_author": True
        },
        {
            "title": "A water-soluble label for food products prevents packaging waste and counterfeiting",
            "authors": "J. Kim et al.",
            "journal": "Nature Food",
            "year": "2024",
            "impact_factor": 21.9,
            "volume": "5",
            "pages": "293-300",
            "is_first_author": True
        },
        {
            "title": "Anti-aliased metasurfaces beyond the Nyquist limit",
            "authors": "J. Kim et al.",
            "journal": "Nature Communications",
            "year": "2025",
            "impact_factor": 15.7,
            "volume": "16",
            "pages": "411",
            "is_first_author": True
        },
        {
            "title": "Amorphous to crystalline transition in nanoimprinted sol-gel titanium oxide metasurfaces",
            "authors": "J. Kim et al.",
            "journal": "Advanced Materials",
            "year": "2024",
            "impact_factor": 26.8,
            "volume": "36",
            "pages": "2405378",
            "is_first_author": True
        },
        {
            "title": "Dynamic hyperspectral holography enabled by inverse-designed metasurfaces with oblique helicoidal cholesterics",
            "authors": "J. Kim et al.",
            "journal": "Advanced Materials",
            "year": "2024",
            "impact_factor": 26.8,
            "volume": "36",
            "pages": "2311785",
            "is_first_author": True
        },
        {
            "title": "Multicolor and 3D holography generated by inverse-design single-cell metasurfaces",
            "authors": "J. Kim et al.",
            "journal": "Advanced Materials",
            "year": "2023",
            "impact_factor": 26.8,
            "volume": "35",
            "pages": "2208520",
            "is_first_author": True
        },
        {
            "title": "Metasurfaces-driven hyperspectral imaging via multiplexed plasmonic resonance energy transfer",
            "authors": "J. Kim et al.",
            "journal": "Advanced Materials",
            "year": "2023",
            "impact_factor": 26.8,
            "volume": "35",
            "pages": "2300229",
            "is_first_author": True
        }
    ]

    for pub in publications_data:
        db_publication = Publication(**pub)
        db.add(db_publication)

    db.commit()
    print("Publications data inserted successfully!")


def insert_conferences_data(db: Session):
    conferences_data = [
        {
            "title": "Nanofabrication Techniques for Advanced Metasurfaces",
            "conference_name": "The 68th International Conference on Electron, Ion and Photon Beam Technology and Nanofabrication (EIPBN)",
            "location": "Savannah, GA, USA",
            "date": "2025-05",
            "presentation_type": "oral, poster"
        },
        {
            "title": "Next-Generation Display Technologies",
            "conference_name": "Consumer Electronics Show (CES)",
            "location": "Las Vegas, NV, USA",
            "date": "2025-01",
            "presentation_type": "exhibition"
        },
        {
            "title": "Advanced Metasurface Applications",
            "conference_name": "The 24nd International Meeting on Information Display (IMID 2024)",
            "location": "Jeju, Korea",
            "date": "2024-08",
            "presentation_type": "poster",
            "award": "Best Poster Award"
        },
        {
            "title": "Plasmonics for Nanophotonics",
            "conference_name": "Gordon Research Conference (GRC) - Plasmonics and Nanophotonics",
            "location": "Newry, ME, USA",
            "date": "2024-07",
            "presentation_type": "poster"
        },
        {
            "title": "Materials Science Applications",
            "conference_name": "MRS Fall Meeting",
            "location": "Boston, USA",
            "date": "2023-11",
            "presentation_type": "two oral, one poster"
        },
        {
            "title": "Information Display Technologies",
            "conference_name": "The 23nd International Meeting on Information Display (IMID 2023)",
            "location": "Busan, Korea",
            "date": "2023-08",
            "presentation_type": "oral",
            "award": "KIDS Award (Gold)"
        },
        {
            "title": "Global Technology Innovations",
            "conference_name": "Samsung Global Technology Symposium (GTS)",
            "location": "Seoul, Korea",
            "date": "2023-04",
            "presentation_type": "poster",
            "award": "Link Award"
        },
        {
            "title": "Advanced Materials Research",
            "conference_name": "MRS Fall Meeting",
            "location": "Boston, USA",
            "date": "2022-11",
            "presentation_type": "oral"
        },
        {
            "title": "Display Technology Innovations",
            "conference_name": "The 22nd International Meeting on Information Display (IMID 2022)",
            "location": "Busan, Korea",
            "date": "2022-08",
            "presentation_type": "oral",
            "award": "KIDS Award (Gold)"
        },
        {
            "title": "Nanotechnology Applications",
            "conference_name": "The 20th International Nanotech Symposium and Nano-Convergence Expo (Nano Korea 2022)",
            "location": "Ilsan, Korea",
            "date": "2022-07",
            "presentation_type": "oral"
        },
        {
            "title": "Micro and Nano Engineering",
            "conference_name": "The 47rd Micro and Nano Engineering (MNE 2021)",
            "location": "Italy",
            "date": "2021-09",
            "presentation_type": "oral"
        },
        {
            "title": "Information Display Research",
            "conference_name": "The 21nd International Meeting on Information Display (IMID 2021)",
            "location": "Busan, Korea",
            "date": "2021-08",
            "presentation_type": "poster"
        },
        {
            "title": "Precision Engineering",
            "conference_name": "International Conference on PRecision Engineering and Sustainable Manufacturing (PRESM 2021)",
            "location": "Jeju, Korea",
            "date": "2021-07",
            "presentation_type": "poster",
            "award": "Best Poster Award"
        },
        {
            "title": "Manufacturing Technology",
            "conference_name": "The Korean Society of Manufacturing Technology Engineers (KSMTE) Fall Meeting",
            "location": "Gangneung, Korea",
            "date": "2021-07",
            "presentation_type": "poster"
        },
        {
            "title": "Mechanical Engineering Research",
            "conference_name": "Korean Society of Mechanical Engineers (KSME) Spring Meeting",
            "location": "Busan, Korea",
            "date": "2021-05",
            "presentation_type": "oral",
            "award": "Best Paper Award"
        }
    ]

    for conf in conferences_data:
        db_conference = Conference(**conf)
        db.add(db_conference)

    db.commit()
    print("Conferences data inserted successfully!")


def main():
    db = SessionLocal()
    try:
        print("Inserting initial data...")
        insert_education_data(db)
        insert_experience_data(db)
        insert_awards_data(db)
        insert_publications_data(db)
        insert_conferences_data(db)
        print("All data inserted successfully!")
    except Exception as e:
        print(f"Error inserting  {e}")
        db.rollback()
    finally:
        db.close()


def main():
    """메인 함수"""
    print("🔧 데이터베이스 연결 확인 중...")

    if not test_db_connection():
        print("❌ 데이터베이스 연결에 실패했습니다.")
        return

    print("📊 테이블 생성 중...")
    create_db_and_tables()

    db = get_db_session()
    try:
        print("📝 초기 데이터 삽입 중...")
        insert_education_data(db)
        insert_experience_data(db)
        insert_awards_data(db)
        insert_publications_data(db)
        insert_conferences_data(db)
        print("🎉 모든 데이터가 성공적으로 삽입되었습니다!")
    except Exception as e:
        print(f"❌ 데이터 삽입 중 오류 발생: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
