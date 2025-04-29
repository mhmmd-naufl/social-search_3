import asyncio
from playwright.async_api import async_playwright

async def scrape_instagram_by_hashtag(tag: str, max_links: int = 10):
    url = f"https://www.instagram.com/explore/tags/{tag}/"
    print(f"Scraping: {url}")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Instagram sering redirect login, pakai User-Agent modern
        await page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        })

        await page.goto(url, timeout=60000)
        
        try:
            await page.wait_for_selector("article a", timeout=15000)
        except Exception as e:
            print(f"Gagal memuat artikel: {e}")
            await browser.close()
            return []

        # Scroll untuk load lebih banyak konten (jika perlu)
        for _ in range(3):
            await page.mouse.wheel(0, 10000)
            await asyncio.sleep(1)

        # Ambil semua link ke post (pake .map untuk ambil href saja)
        links = await page.eval_on_selector_all(
            "article a",
            "elements => elements.map(e => e.href)"
        )

        await browser.close()

        # Ambil hanya yang unik dan batas jumlahnya
        unique_links = list(dict.fromkeys(links))
        return unique_links[:max_links]

# Contoh pemanggilan
if __name__ == "__main__":
    tag = "kulinerjakarta"
    hasil = asyncio.run(scrape_instagram_by_hashtag(tag))
    print("\nHasil postingan:")
    for link in hasil:
        print(link)
