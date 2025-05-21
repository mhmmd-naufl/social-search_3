import os

PATH = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
CHROMEDRIVER_PATH = "C:/chromedriver-win64/chromedriver.exe"

SEARCH_API = (
    "https://www.tiktok.com/api/search/general/full/?"
    "aid=1988&app_language=en&app_name=tiktok_web&browser_language=en-US&"
    "browser_name=Mozilla&browser_online=true&browser_platform=Win32&"
    "browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20"
    "AppleWebKit%2F537.36%20%28KHTML%2C%20Gecko%29%20Chrome%2F135.0.0.0%20"
    "Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&count=30&"
    "cursor={cursor}&device_platform=web_pc&focus_state=true&from_page=search&"
    "history_len=3&is_fullscreen=false&is_page_visible=true&keyword={keyword}&"
    "os=windows&priority_region=®ion=ID&screen_height=1050&screen_width=1680&"
    "tz_name=Asia%2FJakarta&user_is_login=false"
)

COMMENTS_API = (
    "https://www.tiktok.com/api/comment/list/?"
    "WebIdLastTime=1745468006&aid=1988&app_language=en&app_name=tiktok_web&aweme_id={video_id}&"
    "browser_language=en-US&browser_name=Mozilla&browser_online=true&browser_platform=Win32&"
    "browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20"
    "AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F135.0.0.0%20"
    "Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&count=20&"
    "cursor=0&data_collection_enabled=true&device_id=7496727975040796178&device_platform=web_pc&"
    "focus_state=true&from_page=video&history_len=3&is_fullscreen=false&is_page_visible=true&"
    "odinId=7496727857532666898&os=windows&priority_region=&referer=®ion=ID&screen_height=1050&screen_width=1680&"
    "tz_name=Asia%2FJakarta&user_is_login=false&verifyFp=verify_m9uul3hy_MUW0yaqI_d9uZ_4Plw_8QPG_fZD1av698o11&"
    "msToken=oLandq46SdFmJhodB5UJy5hbm1vzXXQs8AHIBPhat_--QmQ5eD-S3M20euY5jPP8TG4o3NT3XR_hUvoATGpcP-"
    "XMqoOHqbkTSjntMyLnOUglrlgtp7bNrnfDkevTueEi4EMGusJl2tUqt69-iTbTSg==&X-Bogus=DFSzswVYyAhANSo9Cayq9y3SsZDI&X-"
    "Gnarly=M/p/wtWYD29qKpbn0td6VM7-Dj8mtlNcKF47EP3jHOnaDMCJPRuYuWt0RbRNWAUNlc19-"
    "Y/noOaTTPcDQ9ECcM/mBI2juOCBvkw9WpYNYbdsynPxGNqzBTSKPyF0mE0JrQ8EbvbPgYbSucMGHVHFUD8uhkIrsYQ6tO86Czb/sriMsF0ZswQt7a8/"
    "UMquGhV-FwKToBfVO-4JQYcl7H6sYrhUFmMLfm-TwHkymJFBbP-/x2yN/0Fn-SKz18/D/rU5NjVN0fVyaXq-"
)

HEADERS = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.8",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "referer": "https://www.tiktok.com/",
}