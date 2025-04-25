import requests, json

post_url = "https://www.tiktok.com/@ct.aisyahh/video/7488191938156449031"

post_id = post_url.split("/")[-1]

headers = {
  'accept' : '*/*',
  'accept-encoding' : 'gzip, deflate, br, zstd',
  'accept-language': 'en-US,en;q=0.8',
  'cookie': 'tt_chain_token=lhTxxjE0jNYlurACiG0j/A==; passport_csrf_token=ec14d72b9648dc07957d9feeeb4cd0fd; passport_csrf_token_default=ec14d72b9648dc07957d9feeeb4cd0fd; odin_tt=30eb077673b7b86369b3ef93f5625b48a28d6055f4e3810e84f2cd113931cfc12e04feb5f6e2b737229f638bb1a1e794af7fc9c6b9db17d6a84566527f98153e28ed59a655663cab601c4ff14e7846ae; tiktok_webapp_theme_source=auto; tiktok_webapp_theme=dark; delay_guest_mode_vid=8; tt_csrf_token=YBcgewsR-aYED_lLKek7ON4bCZQWr9p5Jicw; perf_feed_cache={%22expireTimestamp%22:1745733600000%2C%22itemIds%22:[%227493683042469301522%22%2C%227468639987194547463%22%2C%227467498149133782278%22]}; ttwid=1%7COU943zTBlk33c8Lju-fHz5X74fZLf51ne5k81bfPZPM%7C1745564295%7Cecec09cafb17208652dcb6d665543efeebc797aab678ed1131c01b3e8a053827; msToken=zX_wo2vUhgjjxXotsDDCSfjtw3SW3cgMnP9JB90VVioQDCbcyzXxnfDYZydtBbqSc_rClrgPSPKNUYLo5n5nwiG9gvHxgLLKNjMEFGkeWFMn0pXpXoZCcr-TySz0ASRDF6CJxY7I2Xi3IzVVdh-Qudc=; msToken=zX_wo2vUhgjjxXotsDDCSfjtw3SW3cgMnP9JB90VVioQDCbcyzXxnfDYZydtBbqSc_rClrgPSPKNUYLo5n5nwiG9gvHxgLLKNjMEFGkeWFMn0pXpXoZCcr-TySz0ASRDF6CJxY7I2Xi3IzVVdh-Qudc=',
  'priority': 'u=1, i',
  'referer': 'post_url = https://www.tiktok.com/@ct.aisyahh/video/7488191938156449031',
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
    info = response.json()
    raw_data = info
    
    comments = []
    for c in raw_data.get("comments", []):
        comments.append({
            "comment_id": c.get("cid"),
            "text": c.get("text"),
            "like_count": c.get("digg_count"),
            "user_id": c.get("user", {}).get("user_id"),
            "username": c.get("user", {}).get("unique_id"),
            "nickname": c.get("user", {}).get("nickname")
        })
    
    for comment in comments:
        print("-", comment["username"], ":", comment["text"])

    with open('output_filtered.json', 'w', encoding='utf-8') as f:
        json.dump(comments, f, ensure_ascii=False, indent=4)

req(post_id)
