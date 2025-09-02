# URLS
IMG_BASE_URL = "https://panodata8.panomax.com/cams/2527/{year}/{month}/{day}/{hour}-{minute}-{second}_hd_3_0.jpg"
API_PANOMAX_URL = "https://api.panomax.com/1.0/cams/2527/images/day"

# Schedules
WEEKDAY_OPEN_HOUR = (17, 30)  # 17:30
WEEKDAY_CLOSE_HOUR = (19, 0)  # 19:00

WEEKEND_OPEN_HOUR = (8, 0)    # 08:00
WEEKEND_CLOSE_HOUR = (19, 0)  # 19:00

# ROI of track snapshot (y1:y2, x1:x2)
ROI_COORDS = (432, 464, 848, 896)

# Range of HSV masks
LOWER_GREEN_MASK_RANGE = (35,50,50)
UPPER_GREEN_MASK_RANGE = (85,255,255)
LOWER_YELLOW_MASK_RANGE = (20,50,50)
UPPER_YELLOW_MASK_RANGE = (35,255,255)
LOWER_RED1_MASK_RANGE = (0,50,50)
UPPER_RED1_MASK_RANGE = (10,255,255)
LOWER_RED2_MASK_RANGE = (170,50,50)
UPPER_RED2_MASK_RANGE = (180,255,255)

# threshold of pixels detected
COLOR_THRESHOLD = 50

