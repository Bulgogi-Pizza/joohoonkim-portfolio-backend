import os
import sys

# 프로젝트 루트 디렉토리를 Python 경로에 추가
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from sqlmodel import Session
from app.database import engine, create_db_and_tables, test_db_connection
from app.models import Publication


def parse_authors_contribution(authors_str):
    """저자 문자열에서 기여도 정보를 파싱"""
    is_first_author = False
    is_corresponding = False
    is_equal_contribution = False

    # Joohoon Kim이 first author인지 확인
    if authors_str.startswith("Joohoon Kim"):
        is_first_author = True
    elif "Joohoon Kim*" in authors_str:
        is_equal_contribution = True

    # Corresponding author 확인 (+표시)
    if "Junsuk Rho+" in authors_str:
        is_corresponding = True

    # Contribution type 결정
    if is_first_author:
        contribution_type = "first-author"
    elif is_corresponding:
        contribution_type = "corresponding"
    elif is_equal_contribution:
        contribution_type = "equal-contribution"
    else:
        contribution_type = "co-author"

    return is_first_author, is_corresponding, is_equal_contribution, contribution_type


def get_db_session():
    """데이터베이스 세션을 생성합니다."""
    return Session(engine)


def insert_complete_publications_data():
    publications_data = [
        # Under submission (상태: under-submission)
        {
            "number": 66,
            "title": "Wide-field-of-view, switchable, multi-dimensional light-field display using a metasurface lenticular lens",
            "authors": "Seokil Moon*, Joohoon Kim*, Youngjin Jo*, Juwon Seo, Kyungtae Kim, Chang-Kun Lee+, Junsuk Rho+",
            "journal": "Nature", "year": "2025", "status": "under-submission",
            "featured_info": "in revision"
        },
        {
            "number": 65,
            "title": "Nanoprinting metasurfaces with engineered optical materials",
            "authors": "Dong Kyo Oh*, Hyunjung Kang*, Dohyun Kang*, Joohoon Kim*, Junsuk Rho+",
            "journal": "Nature Review Materials", "year": "2025",
            "status": "under-submission", "featured_info": "in revision"
        },
        {
            "number": 64,
            "title": "Polariton condensate far-detuned from exciton resonance in WS2 bound states in the continuum",
            "authors": "Junghyun Sung*, Joohoon Kim*, Ho Seung Lee, Woo Hun Choi, Minsu Jeong, Jihae Lee, Seokwoo Kim, Dong-Jin Shin, Daegwang Choi, Junsuk Rho+, Su-Hyun Gong+, Hyun Gyu Song+",
            "journal": "Nature Communications", "year": "2025",
            "status": "under-submission", "featured_info": "in revision"
        },
        {
            "number": 63,
            "title": "Roll-to-roll manufacturing of 1 cm visible metalenses with industrial-level throughput of 300 unit per second",
            "authors": "Trung Hoang*, Yujin Park*, Joohoon Kim*, Han Truong, Kyungtae Kim, Dohyun Kang, Gyoseon Jeon, Kyung-il Lee, Dong Hyun Yoon, Sajjan Parajuli, Inki Kim+, Junsuk Rho+, Gyoujin Cho+",
            "journal": "Nature", "year": "2025", "status": "under-submission",
            "featured_info": "in revision"
        },
        {
            "number": 62,
            "title": "Sustainable manufacturing of optical metasurfaces with atomic layer coated high-index resin composite",
            "authors": "Minseok Choi*, Hyujung Kang*, Dohyun Kang*, Joohoon Kim, Junsuk Rho+",
            "journal": "PhotoniX", "year": "2025", "status": "under-submission",
            "featured_info": "in review"
        },

        # 2025 Published
        {
            "number": 61,
            "title": "Compact eye camera with two-third wavelength phase-delay metalens",
            "authors": "Jeong-Geun Yun*, Hyunjung Kang*, Kyookeun Lee, Youngmo Jeong, Eunji Lee, Joohoon Kim, Minseok Choi, Bonkon Koo, Doyoun Kim, Jongchul Choi, Junsuk Rho+",
            "journal": "Nature Communications", "year": "2025",
            "status": "in-press"
        },
        {
            "number": 60,
            "title": "Metasurface absorber-emitter pair-integrated high-efficiency thermophotovoltaic system",
            "authors": "Sumbel Ijaz*, Dohyun Kang*, Ahsan Sarwar Rana*, Joohoon Kim, Muhammad Tariq Saeed Chani, Muhammad Zubair+, Qammer H. Abbassi+, Muhammad Qasim Mehmood+, Junsuk Rho+",
            "journal": "ACS Photonics", "year": "2025", "status": "in-press"
        },
        {
            "number": 59,
            "title": "Ultraviolet-visible spin-resolved chip-scale spectroscopy",
            "authors": "Nasir Mahmood*, Yujin Park*, Naureen Butt*, Joohoon Kim, Dongliong Gao, Muhammad Zubair, Tauseef Tauqeer+, Lei Gao+, Muhammad Qasim Mehmood+, Junsuk Rho+",
            "journal": "Advanced Functional Materials", "year": "2025",
            "status": "in-press"
        },
        {
            "number": 58,
            "title": "Single-layer waveguide display using achromatic metagratings for full-colour augmented reality",
            "authors": "Seokil Moon*, Seokwoo Kim*, Joohoon Kim*, Chang-Kun Lee, Junsuk Rho+",
            "journal": "Nature Nanotechnology", "volume": "20",
            "pages": "747-754", "year": "2025"
        },
        {
            "number": 57,
            "title": "Achromatic metagratings for compact near-eye displays",
            "authors": "Seokwoo Kim*, Joohoon Kim*, Junsuk Rho+",
            "journal": "Nature Nanotechnology", "volume": "20",
            "pages": "721-722", "year": "2025"
        },
        {
            "number": 56, "title": "Nanofabrication for nanophotonics",
            "authors": "Younghwan Yang, Youngsun Jeon, Zhaogang Dong, Joel K. W. Yang, Mahsa Haddadi, Moghaddam, Dai Sik Kim, Dong Kyo Oh, Jihae Lee, Mario Hentschel, Harald Giessen, Dohyun Kang, Gyeongtae Kim, Takuo Tanaka, Yang Zhao, Johannes Bürger, Stefan A. Maier, Haoran Ren, Wooik Jung, Mansoo Choi, Gwangmin Bae, Haomin Chen, Seokwoo Jeon, Jaekyung Kim, Eunji Lee, Hyunjung Kang, Yujin Park, Dang Du Nguyen, Inki kim, Pablo Cencilo-Abad, Debashis Chanda, Xinxin Jing, Na Liu, Irina V. Martynenko, Tim Liedl, Yuna Kwak, Jwa-Min Nam, Sang-Min Park, Teri W. Odom, Hye-Eun Lee, Ryeong Myeong Kim, Ki Tae Nam, Hyunah Kwon, Hyeon-Ho Jeong, Peer Fishcer, Jiwon Yoon, Shin-Hyun Kim, Sangmin Shim, Dasol Lee, Luis A. Pérez, Xiaoyu Qi, Agustin Mihi, Hohyun Keum, Moonsub Shim, Seok Kim, Hanhwi Jang, Yeon Sik Jung, Christian Rossner, Tobias A. F. König, Andreas Fery, Zhiwei Li, Koray Aydin, Chad A. Mirkin, Junhwa seong, Nara Jeon, Zhiyun Xu, Tian Gu, Juejun Hu, Hyunghan Kwon, Hojoong Jung, Hossein Alijan, Igor Aharonovich, Joohoon Kim, Junsuk Rho+",
            "journal": "ACS Nano", "volume": "19", "pages": "12491-12605",
            "year": "2025", "featured_info": "Review Paper"
        },
        {
            "number": 55,
            "title": "Roll-to-plate printable RGB achromatic metalens for wide-field-of-view holographic near-eye displays",
            "authors": "Minseok Choi*, Joohoon Kim*, Seokil Moon*, Kilsoo Shin*, Seung-Woo Nam, Yujin Park, Dohyun Kang, Gyoseon Jeon, Kyung-il Lee, Dong Hyun Yoon, Yoonchan Jeong, Chang-Kun Lee, Junsuk Rho+",
            "journal": "Nature Materials", "volume": "24", "pages": "535-543",
            "year": "2025",
            "featured_info": "Featured as Cover Article of 2025 April issue"
        },
        {
            "number": 54,
            "title": "Dual-band metasurface-based structured light generations for futuristic communication applications",
            "authors": "Muhammad Danial Shafqat*, Yujin Park*, Nasir Mahmood*, Joohoon Kim, Dohyun Kang, Rehan Hafiz, Dongliang Gao, Humberto Cabrera, Muhammad Qasim Mehmood+, Lei Gao+ and Junsuk Rho+",
            "journal": "Small Science", "volume": "5", "pages": "2400524",
            "year": "2025"
        },
        {
            "number": 53,
            "title": "Polarization-controlled multifunctional metasurfaces for ultraviolet-visible dual-band imaging",
            "authors": "Naureen Butt*, Joohoon Kim*, Nasir Mahmood*, Yujin Park, Dohyun Kang, Dongliong Gao, Muhammad Zubair, Tauseef Tauqeer+, Muhammad Qasim Mehmood+, Lei Gao+, Junsuk Rho+",
            "journal": "Advanced Functional Materials", "volume": "35",
            "pages": "2410512", "year": "2025"
        },
        {
            "number": 52,
            "title": "Tape-assisted residual layer-free one-step nanoimprinting of high-index hybrid polymer for optical loss-suppressed metasurfaces",
            "authors": "Yujin Park, Joohoon Kim, Younghwan Yang, Dong Kyo Oh, Hyunjung Kang, Hongyoon Kim, Junsuk Rho+",
            "journal": "Advanced Science", "volume": "12", "pages": "2409371",
            "year": "2025",
            "featured_info": "Featured as Inside Front Cover Article of 2025 March 10 issue"
        },
        {
            "number": 51,
            "title": "Large-area floating display with wafer-scale manufactured metalens arrays",
            "authors": "Joohoon Kim, Jungkwuen An, Wonjoong Kim, Junhwa Seong, Yujin Park, Eunji Lee, Seokwoo Kim, Seokil Moon, Chang-Kun Lee, Heon Lee, Junsuk Rho+",
            "journal": "Laser and Photonics Reviews", "volume": "19",
            "pages": "2401425", "year": "2025"
        },
        {
            "number": 50,
            "title": "Bound-states-in-the-continuum-induced directional photoluminescence with polarization singularity in WS2 monolayers",
            "authors": "Jihae Lee*, Minsu Jeong*, Jaehyuck Jang, Joohoon Kim, Jungho Mun, Xiangxin Gong, Rouli Fang, Yuhui Yang, Sang Hoon Chae, Sejeong Kim+ and Junsuk Rho+",
            "journal": "Nano Letters", "volume": "25", "pages": "861-867",
            "year": "2025"
        },
        {
            "number": 49,
            "title": "12″ wafer-scale mass-manufactured metal-insulator-metal reflective metaholograms by nanotransfer printing",
            "authors": "Chanwoong Park*, Eunji Lee*, Joohoon Kim*, Wonjoong Kim, Hyoin Song, Hansang Sung, Seungyeon Lee, Jaein Park, Trevon Badloe, Junsuk Rho+, Heon Lee+",
            "journal": "ACS Applied Materials and Interfaces", "volume": "17",
            "pages": "3749-3756", "year": "2025"
        },
        {
            "number": 48,
            "title": "Anti-aliased metasurfaces beyond the Nyquist limit",
            "authors": "Seokwoo Kim*, Joohoon Kim*, Kyungtae Kim*, Minsu Jeong, Junsuk Rho+",
            "journal": "Nature Communications", "volume": "16", "pages": "411",
            "year": "2025", "arxiv": "2406.11261"
        },

        # 2024
        {
            "number": 47,
            "title": "Amorphous to crystalline transition in nanoimprinted sol-gel titanium oxide metasurfaces",
            "authors": "Joohoon Kim*, Wonjoong Kim*, Minseok Choi*, Yujin Park, Dohyun Kang, Eunji Lee, Chanwoong Park, Hansang Sung, Heon Lee+, Junsuk Rho+",
            "journal": "Advanced Materials", "volume": "36", "pages": "2405378",
            "year": "2024"
        },
        {
            "number": 46,
            "title": "Deep-learning-driven end-to-end metalens imaging",
            "authors": "Joonhyuk Seo*, Jaegang Jo*, Joohoon Kim*, Joonho Kang*, Chanik Kang, Seong-Won Moon, Eunji Lee, Jehyung Hong, Junsuk Rho+, Haejun Chung+",
            "journal": "Advanced Photonics", "volume": "6", "pages": "066002",
            "year": "2024", "arxiv": "2312.02669"
        },
        {
            "number": 45,
            "title": "Wavelength-multiplexed orbital angular momentum meta-holography",
            "authors": "Jaehyuck Jang*, Seong-Won Moon*, Joohoon Kim*, Jungho Mun, Stefan A. Maier, Haoran Ren, Junsuk Rho+",
            "journal": "PhotoniX", "volume": "5", "pages": "27", "year": "2024"
        },
        {
            "number": 44,
            "title": "Dynamic hyperspectral holography enabled by inverse-designed metasurfaces with oblique helicoidal cholesterics",
            "authors": "Joohoon Kim*, Jun-Hyung Im*, Sunae So*, Yeongseon Choi, Hyungjung Kang, Young-Ki Kim+, Junsuk Rho+",
            "journal": "Advanced Materials", "volume": "36", "pages": "2311785",
            "year": "2024"
        },
        {
            "number": 43,
            "title": "Liquid crystal-integrated metasurfaces for an active photonic platform",
            "authors": "Dohyun Kang*, Hyeongsu Heo*, Younghwan Yang*, Junhwa Seong, Hongyoon Kim, Joohoon Kim, Junsuk Rho+",
            "journal": "Opto-Electronic Advances", "volume": "7",
            "pages": "230216", "year": "2024", "featured_info": "Review Paper"
        },
        {
            "number": 42,
            "title": "Tailoring high-refractive-index nanocompistes for manufacturing of ultraviolet metasurfaces",
            "authors": "Hyungjung Kang*, Dong Kyo Oh*, Nara Jeon*, Joohoon Kim, Hongyoon Kim, Trevon Badloe, Junsuk Rho+",
            "journal": "Microsystems and Nanoengineering", "volume": "10",
            "pages": "53", "year": "2024"
        },
        {
            "number": 41,
            "title": "A water-soluble label for food products prevents packaging waste and counterfeiting",
            "authors": "Joohoon Kim*, Hongyoon Kim*, Hyunjung Kang*, Wonjoong Kim*, Yi Chen, Jonghyun Choi+, Heon Lee+, Junsuk Rho+",
            "journal": "Nature Food", "volume": "5", "pages": "293-300",
            "year": "2024",
            "featured_info": "Featured as Cover Article of 2024 April issue"
        },
        {
            "number": 40,
            "title": "8″ wafer-scale, centimeter-sized, high-efficiency metalenses in the ultraviolet",
            "authors": "Joohoon Kim*, Yeseul Kim*, Wonjoong Kim*, Dong Kyo Oh, Dohyun Kang, Junhwa Seong, Jeong Woo Shin, Dohyun Go, Chanwoong Park, Hyoin Song, Jihwan An, Heon Lee+, Junsuk Rho+",
            "journal": "Materials Today", "volume": "73", "pages": "9-15",
            "year": "2024",
            "featured_info": "Featured in Front Cover Article of 2024 March-April issue"
        },
        {
            "number": 39,
            "title": "Wafer-scale manufacturing of near-infrared metalenses",
            "authors": "Seong-Won Moon*, Joohoon Kim*, Chanwoong Park*, Wonjoong Kim*, Younghwan Yang, Jaekyung Kim, Seokho Lee, Minseok Choi, Hansang Sung, Jaein Park, Hyoin Song, Heon Lee+, Junsuk Rho+",
            "journal": "Laser and Photonics Reviews", "volume": "18",
            "pages": "2300929", "year": "2024",
            "featured_info": "Featured as Frontispiece Cover Article of 2024 April 8 issue"
        },
        {
            "number": 38,
            "title": "A high-throughput method for large scale meta-holograms via one-step printing",
            "authors": "Chanwoong Park*, Wonjoong Kim*, Yeseul Kim*, Hansang Sung, Jaein Park, Hyoin Song, Joohoon Kim, Dong Kyo Oh, Hyunjung Kang, Nara Jeon, Junsuk Rho+, Heon Lee+",
            "journal": "Advanced Optical Materials", "volume": "12",
            "pages": "2301562", "year": "2024"
        },
        {
            "number": 37, "title": "Roadmap for optical metasurfaces",
            "authors": "Arseniy I. Kuznetsov+, Mark L. Brongersma+, Jin Yao, Mu Ku Chen, Uriel Levy, Din Ping Tsai, Nikolay I. Zheludev, Andrei Faraon, Amir Arabi, Nanfang Yu, Debashis Chanda, Kenneth Crozier, Alexander V. Kildishev, Hao Wang, Joel K. W. Yang, Jason Valentine, Patrice Genevet, Jonathan A. Fan, Owel D. Miller, Steven G. Johnson, Arka Majumdar, Johannes E. Froch, David Brady, Felix Heide, Ashok Veeraraghavan, Nader Engheta, Andrea Alu, Albert Polman, Harry A. Atwater, Prachi Thureja, Ramon Paniagua-Dominguez, Son Tung Ha, Angela Barreda, Jon Schuller, Isabelle Staude, Gustavo Grinblat, Yuri Kivshar, Samuel Peana, Susanne F. Yelin, Alexander Senichev, Vladimir M. Shalaev, Soham Saha, Alexandra Boltasseva, Junsuk Rho, Dong Kyo Oh, Joohoon Kim, Junghyun Park, Robert Devlin, Ragip Pala",
            "journal": "ACS Photonics", "volume": "11", "pages": "816-865",
            "year": "2024", "featured_info": "Review Paper"
        },
        {
            "number": 36,
            "title": "Spin-selective angular dispersion control in dielectric metasurfaces for multi-channel meta-holographic displays",
            "authors": "Sabiha Latif*, Joohoon Kim*, Hafiz Saad Khaliq*, Nasir Mahmood, Muhammad Afnan Ansari, Xianzhong Chen, Jehan Akbar, Trevon Badloe, Muhammad Zubair+, Yehia Massoud+, Muhammad Qasim Mehmood+, Junsuk Rho+",
            "journal": "Nano Letters", "volume": "24", "pages": "708-714",
            "year": "2024"
        },

        # 2023
        {
            "number": 35,
            "title": "Metasurfaces-driven hyperspectral imaging via multiplexed plasmonic resonance energy transfer",
            "authors": "Inki Kim*, Hongyoon Kim*, Seungyeon Han*, Joohoon Kim*, Yangkyu Kim, Seonghyeon Eom, Aleksandr Barulin, Inhee Choi+, Junsuk Rho+, Luke P. Lee+",
            "journal": "Advanced Materials", "volume": "35", "pages": "2300229",
            "year": "2023",
            "featured_info": "Featured as Front Cover Article of 2023 August 11 issue"
        },
        {
            "number": 34,
            "title": "Bright-field and edge-enhanced bioimaging using an electrically tunable dual-mode metalens",
            "authors": "Trevon Badloe*, Yeseul Kim*, Joohoon Kim*, Hyemi Park, Aleksandr Barulin, Yen N. Diep, Hansang Cho, Won-Sik Kim, Young-Ki Kim, Inki Kim+, Junsuk Rho+",
            "journal": "ACS Nano", "volume": "17", "pages": "14678-14685",
            "year": "2023"
        },
        {
            "number": 33,
            "title": "Arbitrarily structured quantum emission with a multifunctional metalens",
            "authors": "Chi Li*, Jaehyuck Jang*, Trevon Badloe*, Tieshan Yang, Joohoon Kim, Jaekyung Kim, Minh Nguyen, Stefan A. Maier, Junsuk Rho+, Haoran Ren+, Igor Aharonovich",
            "journal": "eLight", "volume": "3", "pages": "19", "year": "2023",
            "arxiv": "2209.04571"
        },
        {
            "number": 32,
            "title": "Integrated metasurfaces for re-envisioning a near-future disruptive optical platform",
            "authors": "Younghwan Yang*, Junhwa Seong*, Minseok Choi*, Junkyeong Park*, Gyeongtae Kim, Hongyoon Kim, Junhyeon Jeong, Chunghwan Jung, Joohoon Kim, Gyoseon Jeon, Kyung-il Lee, Dong Hyun Yoon, Junsuk Rho+",
            "journal": "Light: Science and Applications", "volume": "12",
            "pages": "152", "year": "2023", "featured_info": "Review Paper"
        },
        {
            "number": 31,
            "title": "Realization of high aspect ratio metalenses by facile nanoimprint lithography using water-soluble stamps",
            "authors": "Hojung Choi*, Joohoon Kim*, Wonjoong Kim, Junhwa Seong, Chanwoong Park, Minseok Choi, Nakhyun Kim, Jisung Ha, Cheng-Wei Qiu, Junsuk Rho+, Heon Lee+",
            "journal": "PhotoniX", "volume": "4", "pages": "18", "year": "2023"
        },
        {
            "number": 30,
            "title": "Spin-isolated ultraviolet-visible dynamic metaholographic displays with liquid crystal modulators",
            "authors": "Aqsa Asad*, Joohoon Kim*, Hafiz Saad Khaliq*, Nasir Mahmood, Jehan Akbar, Muhammad Tariq Saeed Channi, Yeseul Kim, Dongmin Jeon, Muhammad Zubair+, Muhammad Qasim Mehmood+, Yehia Massoud+, Junsuk Rho+",
            "journal": "Nanoscale Horizons", "volume": "8", "pages": "759-766",
            "year": "2023",
            "featured_info": "Featured as Inside Front Cover Article of 2023 June issue"
        },
        {
            "number": 29,
            "title": "Multicolor and 3D holography generated by inverse-design single-cell metasurfaces",
            "authors": "Sunae So*, Joohoon Kim*, Trevon Badloe*, Chihun Lee, Younghwan Yang, Hyunjung Kang, Junsuk Rho+",
            "journal": "Advanced Materials", "volume": "35", "pages": "2208520",
            "year": "2023", "arxiv": "2207.04778"
        },
        {
            "number": 28,
            "title": "Scalable manufacturing of high-index atomic layer-polymer hybrid metasurfaces for metaphotonics in the visible",
            "authors": "Joohoon Kim*, Junhwa Seong*, Wonjoong Kim*, Gun-Yeal Lee, Seokwoo Kim, Hongyoon Kim, Seong-Won Moon, Dong Kyo Oh, Younghwan Yang, Jeonghoon Park, Jaehyuck Jang, Yeseul Kim, Minsu Jeong, Chanwoong Park, Hojung Choi, Gyoseon Jeon, Kyung-Il Lee, Dong Hyun Yoon, Namkyoo Park, Byoungho Lee, Heon Lee+, Junsuk Rho+",
            "journal": "Nature Materials", "volume": "22", "pages": "474-481",
            "year": "2023", "arxiv": "2208.12665",
            "featured_info": "Featured in News and Views, Nature Photonics"
        },
        {
            "number": 27,
            "title": "One-step printable platform for high-efficiency metasurfaces down to the deep ultraviolet region",
            "authors": "Joohoon Kim*, Wonjoong Kim*, Dong Kyo Oh*, Hyunjung Kang, Hongyoon Kim, Trevon Badloe, Seokwoo Kim, Chanwoong Park, Hojung Choi, Heon Lee+, Junsuk Rho+",
            "journal": "Light: Science and Applications", "volume": "12",
            "pages": "68", "year": "2023"
        },
        {
            "number": 26,
            "title": "Dynamic chiral metasurfaces for broadband phase-gradient holographic displays",
            "authors": "Taimoor Naeem*, Joohoon Kim*, Hafiz Saad Khaliq*, Junhwa Seong, Muhammad Tariq Saeed Chani, Tauseef Tauqeer+, Muhammad Qasim Mehmood+, Yehia Massoud+, Junsuk Rho+",
            "journal": "Advanced Optical Materials", "volume": "11",
            "pages": "2202278", "year": "2023",
            "featured_info": "Featured as Front Cover Article of 2023 March 5 issue"
        },
        {
            "number": 25,
            "title": "UV-visible multifunctional vortex metaplates by breaking conventional rotational symmetry",
            "authors": "Nasir Mahmood*, Joohoon Kim*, Muhammad Ashar Naveed*, Yeseul Kim, Junhwa Seong, Seokwoo Kim, Trevon Badloe, Mahammad Zubair+, Muhammad Qasim Mehmood+, Yehia Massoud+, Junsuk Rho+",
            "journal": "Nano Letters", "volume": "23", "pages": "1195-1201",
            "year": "2023"
        },

        # 2022
        {
            "number": 24,
            "title": "Single-cell-driven tri-channel encryption meta-displays",
            "authors": "Muhammad Qasim Mehmood*, Junhwa Seong*, Muhammad Ashar Naveed*, Joohoon Kim*, Muhammad Zubair+, Kashif Riaz+, Yehia Massoud+, Junsuk Rho+",
            "journal": "Advanced Science", "volume": "9", "pages": "2203962",
            "year": "2022"
        },
        {
            "number": 23,
            "title": "High numerical aperture RGB achromatic metalens in the visible",
            "authors": "Sangwon Baek*, Joohoon Kim*, Yeseul Kim*, Won Seok Cho, Trevon Badloe, Seong-Won Moon, Junsuk Rho+, Jong-Lam Lee+",
            "journal": "Photonics Research", "volume": "10", "pages": "B30-B39",
            "year": "2022"
        },
        {
            "number": 22,
            "title": "Broadband chiro-optical effects for futuristic meta-holographic displays",
            "authors": "Hafiz Saad Khaliq*, Joohoon Kim*, Taimoor Naeem, Kashif Riaz, Trevon Badloe, Junhwa Seong, Jehan Akbar, Muhammad Zubair+, Muhammad Qasim Mehmood+, Yehia Massoud+, Junsuk Rho+",
            "journal": "Advanced Optical Materials", "volume": "10",
            "pages": "2201175", "year": "2022"
        },
        {
            "number": 21,
            "title": "Broad-band polarization-insensitive metasurface holography with a single-phase map",
            "authors": "Isma Javed*, Joohoon Kim*, Muhammad Ashar Naveed*, Dong Kyo Oh, Dongmin Jeon, Inki Kim, Muhammad Zubair+, Yehia Massoudd+, Muhammad Qasim Mehmood+, Junsuk Rho+",
            "journal": "ACS Applied Materials and Interfaces", "volume": "14",
            "pages": "36019-36026", "year": "2022"
        },
        {
            "number": 20,
            "title": "Metasurface holography reaching the highest efficiency limit in the visible via one-step nanoparticle-embedded-resin printing",
            "authors": "Joohoon Kim*, Dong Kyo Oh*, Hongyoon Kim, Gwanho Yoon, Chunghwan Jung, Jaekyung Kim, Trevon Badloe, Hyunjung Kang, Seokwoo Kim, Younghwan Yang, Jihae Lee, Byoungsu Ko, Jong G. Ok, Junsuk Rho+",
            "journal": "Laser and Photonics Reviews", "volume": "16",
            "pages": "2200098", "year": "2022", "arxiv": "2109.01141"
        },
        {
            "number": 19,
            "title": "Single-step fabrication flexible metadisplays for sensitive chemical/biomedical packaging security and beyond",
            "authors": "Muhammad Ashar Naveed*, Joohoon Kim*, Muhammad Afnan Ansari*, Inki Kim, Yehia Massoud, Jaekyung Kim, Dong Kyo Oh, Trevon Badloe, Jihae Lee, Yeseul Kim, Dongmin Jeon, Jonghyun Choi, Muhammad Zubair+, Muhammad Qasim Mehmood+, Junsuk Rho+",
            "journal": "ACS Applied Materials and Interfaces", "volume": "14",
            "pages": "31194-31202", "year": "2022"
        },
        {
            "number": 18,
            "title": "Thermally-curable nanocomposite printing for the scalable manufacturing of dielectric metasurfaces",
            "authors": "Wonjoong Kim*, Gwanho Yoon*, Joohoon Kim*, Heonyeong Jeong, Yeseul Kim, Hojung Choi, Trevon Badloe, Junsuk Rho+ Heon Lee+",
            "journal": "Microsystems and Nanoengineering", "volume": "8",
            "pages": "73", "year": "2022"
        },
        {
            "number": 17,
            "title": "Novel spin-decoupling strategy in liquid crystal-integrated metasurfaces for interactive metadisplays",
            "authors": "Muhammad Ashar Naveed*, Joohoon Kim*, Isma Javaid, Muhammad Afnan Ansari, Junhwa Seong, Yehia Massoud, Trevon Badloe, Inki Kim, Kashif Riaz, Muhammad Zubair, Muhammad Qasim Mehmood+, Junsuk Rho+",
            "journal": "Advanced Optical Materials", "volume": "10",
            "pages": "2200196", "year": "2022"
        },
        {
            "number": 16,
            "title": "Nanostructured chromium-based broadband absorbers and emitters to realize thermally stable solar thermophotovoltaic systems",
            "authors": "Muhammad Aamir Abbas*, Joohoon Kim*, Ahsan Sarwar Rana*, Inki Kim, Bacha Rehman, Zubair Ahmad, Junhwa Seong, Trevon Badloe, Keunhan Park, Muhammad Qasim Mehmood+, Muhammad Zubair+, Junsuk Rho+",
            "journal": "Nanoscale", "volume": "14", "pages": "6425-6436",
            "year": "2022"
        },
        {
            "number": 15,
            "title": "Liquid crystal-powered Mie resonators for electrically tunable photorealistic color gradients and dark blacks",
            "authors": "Trevon Badloe*, Joohoon Kim*, Inki Kim*, Won-Sik Kim*, Wook Sung Kim, Young-Ki Kim+, Junsuk Rho+",
            "journal": "Light: Science and Applications", "volume": "11",
            "pages": "118", "year": "2022",
            "featured_info": "Featured in News and Views, Light: Science and Applications"
        },
        {
            "number": 14,
            "title": "Photonic encryption platform via dual-band vectroial metaholograms in the ultra-violet and visible",
            "authors": "Joohoon Kim, Dongmin Jun, Junhwa Seong, Trevon Badloe, Nara Jeon, Gyeongtae Kim, Jaekyung Kim, Sangwon Baek, Jong-Ram Lee, Junsuk Rho+",
            "journal": "ACS Nano", "volume": "16", "pages": "3546-3553",
            "year": "2022"
        },
        {
            "number": 13,
            "title": "Burr- and etch-free direct machining of shape-controlled micro- and nanopatterns on polyimide films by continuous nanoinscribing for durable flexible devices",
            "authors": "Dong Kyo Oh*, Wonseok Lee*, Hyoungseok Chae, Hyunsoo Chun, Minyoung Lee, Dong Ha Kim, Joohoon Kim, Jaemin Choi, Sangwon Hwang, Minyong Park, Gyubeom Yeon, Sunmin Jung, Junsuk Rho, Jong G. Ok+",
            "journal": "Microelectronic Engineering", "volume": "257",
            "pages": "111740", "year": "2022"
        },
        {
            "number": 12,
            "title": "Tutorial on metalenses for advanced flat optics: Design, fabrication and critical consideration",
            "authors": "Seong-Won Moon*, Chihun Lee*, Younghwan Yang*, Joohoon Kim*, Trevon Badloe, Chunghwan Jung, Gwanho Yoon, Junsuk Rho+",
            "journal": "Journal of Applied Physics", "volume": "131",
            "pages": "091101", "year": "2022", "featured_info": "Review Paper"
        },

        # 2021
        {
            "number": 11,
            "title": "Electrically Tunable Bifocal Metalens with Diffraction-Limited Focusing and Imaging at Visible Wavelengths",
            "authors": "Trevon Badloe*, Inki Kim*, Yeseul Kim*, Joohoon Kim, Junsuk Rho+",
            "journal": "Advanced Science", "volume": "8", "pages": "2102646",
            "year": "2021",
            "featured_info": "Featured as Inside Front Cover Article of 2021 November 4 issue"
        },
        {
            "number": 10,
            "title": "Dual-band operating with heterogeneous meta-atoms in the visible and near-infrared",
            "authors": "Inki Kim*, Heonyeong Jeong*, Joohoon Kim*, Younghwan Yang, Dasol Lee, Trevon Badloe, Gyeongtae Kim, Junsuk Rho+",
            "journal": "Advanced Optical Materials", "volume": "9",
            "pages": "2100609", "year": "2021",
            "featured_info": "Featured as Inside Front Cover Article of 2021 October 4 issue"
        },
        {
            "number": 9,
            "title": "Solution-processible electrode embedding in dynamically inscribed nanopattern (SPEEDIN) for continuous fabrication of scratch-proof flexible electronics",
            "authors": "Wonseok Lee*, Hyoungseok Chae*, Dong Kyo Oh*, Minyoung Lee, Hyunsoo Chun, Gyubeom Yeon, Jaewon Park, Joohoon Kim, Junsuk Rho, Hongseok Youn+, Jong G. Ok+",
            "journal": "Microsystems and Nanoengineering", "volume": "7",
            "pages": "74", "year": "2021"
        },
        {
            "number": 8,
            "title": "Giant chiro-optical responses in multipolar-resonances-based single-layer dielectric metasurface",
            "authors": "Hafiz Saad Khaliq*, Inki Kim*, Joohoon Kim, Taejun Lee, Dong Kyo Oh, Yeseul Kim, Muhammad Zubair, Kashif Riaz, Muhammad Qasim Mehmood+, Junsuk Rho+",
            "journal": "Photonics Research", "volume": "9", "pages": "9",
            "year": "2021"
        },
        {
            "number": 7,
            "title": "Geometric and physical configurations of meta-atoms for advanced metasurface holography",
            "authors": "Joohoon Kim*, Younghwan Yang*, Trevon Badloe, Inki Kim, Gwanho Yoon, Junsuk Rho+",
            "journal": "InfoMat", "volume": "3", "pages": "739", "year": "2021",
            "featured_info": "Review Paper"
        },
        {
            "number": 6,
            "title": "Chiroptical metasurfaces: principles, classification, and applications",
            "authors": "Joohoon Kim*, Ahsan Sarwar Rana*, Yeseul Kim*, Inki Kim, Trevon Badloe, Muhammad Zubair, Muhammad Qasim Mehmood+, Junsuk Rho+",
            "journal": "Sensors", "volume": "21", "pages": "4381",
            "year": "2021", "featured_info": "Review Paper, Editor's Choice"
        },
        {
            "number": 5,
            "title": "Nearly perfect transmissive substractive coloration through the spectral amplification of Mie scattering and lattice resonance",
            "authors": "Taejun Lee*, Joohoon Kim*, Ishwor Koirala, Younghwan Yang, Trevon Badloe, Jaehyuck Jang, Junsuk Rho+",
            "journal": "ACS Applied Materials and Interfaces", "volume": "13",
            "pages": "26299-26307", "year": "2021"
        },
        {
            "number": 4,
            "title": "Manifesting simultaneous optical spin conservation and spin isolation in diatomic metasurface",
            "authors": "Hafiz Saad Khaliq*, Inki Kim*, Joohoon Kim, Dong Kyo Oh, Muhammad Zubair, Kashif Riaz, Muhammad Qasim Mehmood+, Junsuk Rho+",
            "journal": "Advanced Optical Materials", "volume": "9",
            "pages": "2002002", "year": "2021"
        },
        {
            "number": 3,
            "title": "Optical spin-symmetry breaking for high-efficiency directional helicity-multiplexed metaholograms",
            "authors": "Muhammad Ashar Naveed*, Muhammad Afnan Ansari*, Inki Kim*, Trevon Badloe, Joohoon Kim, Dong Kyo Oh, Kashif Riaz, Tauseef Tauqeer, Usman Younis, Murtaza Saleem, Muhammad Sabieh Anwar, Muhammad Zubair, Muhammad Qasim Mehmood+, Junsuk Rho+",
            "journal": "Microsystems and Nanoengineering", "volume": "7",
            "pages": "5", "year": "2021"
        },
        {
            "number": 2,
            "title": "Top-down nanofabrication approaches toward single-digit-nanometer scale structures",
            "authors": "Dong Kyo Oh*, Heonyeong Jeong*, Joohoon Kim*, Yeseul Kim*, Inki Kim, Jong. G. Ok, Junsuk Rho+",
            "journal": "Journal of Mechanical Science and Technology",
            "volume": "35", "pages": "837-839", "year": "2021",
            "featured_info": "Review Paper"
        },

        # 2020
        {
            "number": 1,
            "title": "Structural color switching with a doped indium-gallium-zinc-oxide semiconductor",
            "authors": "Inki Kim*, Juyoung Yun*, Trevon Badloe, Hyuk Park, Taewon Seo, Younghwan Yang, Joohoon Kim, Yoonyoung Chung, Junsuk Rho",
            "journal": "Photonics Research", "volume": "8",
            "pages": "1381-1387", "year": "2020"
        }
    ]

    db = get_db_session()
    try:
        print("📝 전체 Publications 데이터 삽입 중...")

        # 기존 데이터 모두 삭제
        db.query(Publication).delete()
        db.commit()
        print("🗑️ 기존 데이터 삭제 완료")

        for pub_data in publications_data:
            # 기여도 정보 파싱
            is_first, is_corresponding, is_equal, contribution = parse_authors_contribution(
                pub_data["authors"])

            publication = Publication(
                number=pub_data["number"],
                title=pub_data["title"],
                authors=pub_data["authors"],
                journal=pub_data["journal"],
                volume=pub_data.get("volume"),
                pages=pub_data.get("pages"),
                year=pub_data["year"],
                month=pub_data.get("month"),
                doi=pub_data.get("doi"),
                arxiv=pub_data.get("arxiv"),
                is_first_author=is_first,
                is_corresponding_author=is_corresponding,
                is_equal_contribution=is_equal,
                contribution_type=contribution,
                status=pub_data.get("status", "published"),
                featured_info=pub_data.get("featured_info")
            )
            db.add(publication)

        db.commit()
        print("✅ 전체 Publications 데이터 삽입 성공!")
        print(f"📊 총 {len(publications_data)}개의 논문 데이터가 삽입되었습니다.")
    except Exception as e:
        print(f"❌ 데이터 삽입 중 오류 발생: {e}")
        db.rollback()
        raise
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

    insert_complete_publications_data()
    print("🎉 전체 Publication 데이터 삽입이 성공적으로 완료되었습니다!")


if __name__ == "__main__":
    main()
