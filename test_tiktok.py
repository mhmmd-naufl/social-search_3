import requests, json

post_url = "https://www.tiktok.com/@fitrinaia/video/7486411648924749111"

post_id = post_url.split("/")[-1]

headers = {
  'accept' : '*/*',
  'accept-encoding' : 'gzip, deflate, br, zstd',
  'accept-language': 'en-US,en;q=0.8',
  'cookie': 'tt_csrf_token=LRqsRFvn-HjXZKHO8S4ZtO83yKPvjL4t3w4o; tt_chain_token=lhTxxjE0jNYlurACiG0j/A==; s_v_web_id=verify_m9uul3hy_MUW0yaqI_d9uZ_4Plw_8QPG_fZD1av698o11; passport_csrf_token=ec14d72b9648dc07957d9feeeb4cd0fd; passport_csrf_token_default=ec14d72b9648dc07957d9feeeb4cd0fd; odin_tt=30eb077673b7b86369b3ef93f5625b48a28d6055f4e3810e84f2cd113931cfc12e04feb5f6e2b737229f638bb1a1e794af7fc9c6b9db17d6a84566527f98153e28ed59a655663cab601c4ff14e7846ae; tiktok_webapp_theme_source=auto; tiktok_webapp_theme=dark; delay_guest_mode_vid=8; perf_feed_cache={%22expireTimestamp%22:1745650800000%2C%22itemIds%22:[%227491309079789374726%22%2C%227494794866396794119%22%2C%227469338214281661704%22]}; msToken=pQ76zBhd23d8xKl4luIuwsWeBshs4SPcmHLGP0VFWxoaQ7eWRaZP3jjK_CncwTBALfbcPg7TpA_hPTq24KnkLHefwAUqalNfgPwJ5-IGTEcn_ymat2BZI5c0GKqJKcAEvLMg2JYd6eKrT-9Z_g__jA==; ttwid=1%7COU943zTBlk33c8Lju-fHz5X74fZLf51ne5k81bfPZPM%7C1745478572%7C37f8e138cbb79e360831e07272a56b5e18d4ad392d02ec06597281426597cb5a; msToken=oLandq46SdFmJhodB5UJy5hbm1vzXXQs8AHIBPhat_--QmQ5eD-S3M20euY5jPP8TG4o3NT3XR_hUvoATGpcP-XMqoOHqbkTSjntMyLnOUglrlgtp7bNrnfDkevTueEi4EMGusJl2tUqt69-iTbTSg==',
  'priority': 'u=1, i',
  'referer': 'https://www.tiktok.com/@fitrinaia/video/7486411648924749111',
  'sec-ch-ua': '"Brave";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'sec-gpc': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
}

def req(post_id):
  url = f'https://www.tiktok.com/api/comment/list/?WebIdLastTime=1745468006&aid=1988&app_language=en&app_name=tiktok_web&aweme_id={post_id}&browser_language=en-US&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F135.0.0.0%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&count=20&cursor=0&data_collection_enabled=true&device_id=7496727975040796178&device_platform=web_pc&focus_state=true&from_page=video&history_len=3&is_fullscreen=false&is_page_visible=true&odinId=7496727857532666898&os=windows&priority_region=&referer=&region=ID&screen_height=1050&screen_width=1680&tz_name=Asia%2FJakarta&user_is_login=false&verifyFp=verify_m9uul3hy_MUW0yaqI_d9uZ_4Plw_8QPG_fZD1av698o11&webcast_language=en&msToken=oLandq46SdFmJhodB5UJy5hbm1vzXXQs8AHIBPhat_--QmQ5eD-S3M20euY5jPP8TG4o3NT3XR_hUvoATGpcP-XMqoOHqbkTSjntMyLnOUglrlgtp7bNrnfDkevTueEi4EMGusJl2tUqt69-iTbTSg==&X-Bogus=DFSzswVYyAhANSo9Cayq9y3SsZDI&X-Gnarly=M/p/wtWYD29qKpbn0td6VM7-Dj8mtlNcKF47EP3jHOnaDMCJPRuYuWt0RbRNWAUNlc19-Y/noOaTTPcDQ9ECcM/mBI2juOCBvkw9WpYNYbdsynPxGNqzBTSKPyF0mE0JrQ8EbvbPgYbSucMGHVHFUD8uhkIrsYQ6tO86Czb/sriMsF0ZswQt7a8/UMquGhV-FwKToBfVO-4JQYcl7H6sYrhUFmMLfm-TwHkymJFBbP-/x2yN/0Fn-SKz18/D/rU5NjVN0fVyaXq-'
  response = requests.get(url, headers=headers)
  info = response.text
  
  print("Response status code:", response.status_code)
  print("Response text:", response.text)
  
  if response.status_code != 200:
    print("Error: Failed to fetch data from TikTok API")
    print("Status code:", response.status_code)
    print("Response text:", response.text)
    return
  
  raw_data = json.loads(info)
  
  with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(raw_data, f,ensure_ascii=False ,indent=4)
    
  try:
    raw_data = json.loads(info)
  except json.JSONDecodeError as e:
    print("Error decoding JSON:", e)
    print("Response text:", info)
    return

req(post_id)