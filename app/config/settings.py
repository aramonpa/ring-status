"""Ring Status configuration."""

from pathlib import Path
from pydantic import BaseSettings

ROOT_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    IMG_BASE_URL: str = (
        "https://panodata9.panomax.com/cams/2527/{year}/{month:02d}/{day:02d}/{hour:02d}-{minute:02d}-{second:02d}_hd_3_0.jpg"
    )
    API_PANOMAX_URL: str = "https://api.panomax.com/1.0/cams/2527/images/day"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    WEEKDAY_OPEN_HOUR: tuple[int, int] = (17, 30)
    WEEKDAY_CLOSE_HOUR: tuple[int, int] = (19, 0)
    WEEKEND_OPEN_HOUR: tuple[int, int] = (8, 0)
    WEEKEND_CLOSE_HOUR: tuple[int, int] = (19, 0)
    ROI_COORDS: tuple[int, int, int, int] = (432, 464, 848, 896)
    LOWER_GREEN_MASK_RANGE: tuple[int, int, int] = (35, 50, 50)
    UPPER_GREEN_MASK_RANGE: tuple[int, int, int] = (85, 255, 255)
    LOWER_YELLOW_MASK_RANGE: tuple[int, int, int] = (20, 50, 50)
    UPPER_YELLOW_MASK_RANGE: tuple[int, int, int] = (35, 255, 255)
    LOWER_RED1_MASK_RANGE: tuple[int, int, int] = (0, 50, 50)
    UPPER_RED1_MASK_RANGE: tuple[int, int, int] = (10, 255, 255)
    LOWER_RED2_MASK_RANGE: tuple[int, int, int] = (170, 50, 50)
    UPPER_RED2_MASK_RANGE: tuple[int, int, int] = (180, 255, 255)
    COLOR_THRESHOLD: int = 50

    class Config:
        env_file = ROOT_DIR / ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
