from pathlib import Path
from urllib.parse import quote

EXIT_CODE_FAILURE = 1

PATH_PACKAGE = Path(__file__).resolve().parent
PATH_README = Path("README.md")
PATH_ASSETS = Path("Assets") / "Readme"
PATH_PHOTOS = Path("Images") / "Cards"
PATH_DOCUMENTS = Path("Documents")

DOCUMENT_RESUME = "Resume - Sadra.pdf"
DOCUMENT_RESUME_QUANT = "Resume - Sadra 2.pdf"
DOCUMENT_LETTER = "Letter of Recommendation.pdf"
DOCUMENT_THESIS = "PWS - Artificial Intelligence.pdf"

URL_DOCUMENTS = PATH_DOCUMENTS.as_posix()
URL_RESUME = f"{URL_DOCUMENTS}/{quote(DOCUMENT_RESUME)}"
URL_RESUME_QUANT = f"{URL_DOCUMENTS}/{quote(DOCUMENT_RESUME_QUANT)}"
URL_LETTER = f"{URL_DOCUMENTS}/{quote(DOCUMENT_LETTER)}"
URL_THESIS = f"{URL_DOCUMENTS}/{quote(DOCUMENT_THESIS)}"

URL_SITE = "https://sadra.nl"
URL_PROP_CALCULATOR = "https://sadra.nl/prop-calculator"
URL_EMAIL = "mailto:sadra.shameli1@gmail.com"
URL_LINKEDIN = "https://linkedin.com/in/sadrashameli"
URL_YOUTUBE = "https://youtube.com/@SadraShameli"
URL_MINOMARKT = "https://minomarkt.nl"
URL_NOBEARS = "https://www.nobears.com"
URL_BLUE_STAR_PLANNING = "https://bluestarplanning.com"
URL_REPOSITORY_SADRA_NL = "https://github.com/SadraShameli/sadra.nl"
URL_REPOSITORY_SENSORHUB = "https://github.com/SadraShameli/sensorhub"
URL_REPOSITORY_PROJECTAI = "https://github.com/SadraShameli/ProjectAI"
URL_SENSORHUB_ENCLOSURE = "https://github.com/SadraShameli/sensorhub/blob/main/Assets/3D%20Models/Sensor%20Unit/Casing%20body.stl"
URL_VIDEO_LINE_DETECTION = "https://www.youtube.com/watch?v=1142rRZ3rzc"
URL_VIDEO_LIDAR_RANGING = "https://www.youtube.com/watch?v=_C8PnLK2SWA"
URL_VIDEO_INDOOR_TEST = "https://www.youtube.com/shorts/abyVlfAETG0"

BYTES_PER_KIB = 1024
