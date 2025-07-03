import asyncio
import json
from playwright.async_api import async_playwright

LOGIN_STATE = "linkedin_login.json"
GROUP_URL = "https://www.linkedin.com/groups/111111"

async def scrape_group():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50)
        context = await browser.new_context(storage_state=LOGIN_STATE)
        page = await context.new_page()

        print("Navigating to group...")
        await page.goto(GROUP_URL, timeout=120000, wait_until="domcontentloaded")

        print("Scrolling until end...")

        # Wait until groups-core-rail is visible
        await page.wait_for_selector("div.groups-core-rail", timeout=60000)

        previous_count = -1
        same_count_counter = 0

        while True:
            await page.mouse.wheel(0, 3000)
            await asyncio.sleep(2)

            post_elements = await page.locator('div.groups-core-rail div.artdeco-card.mb2').all()
            current_count = len(post_elements)

            print(f"Posts loaded so far: {current_count}")

            if current_count == previous_count:
                same_count_counter += 1
            else:
                same_count_counter = 0
                previous_count = current_count

            if same_count_counter >= 3:
                print("No new posts detected. Reached end.")
                break

        # ✅ Extract raw HTML of each post
        print("Extracting raw HTML of posts...")
        raw_posts = []

        post_elements = await page.locator('div.groups-core-rail div.artdeco-card.mb2').all()
        for post in post_elements:
            try:
                html = await post.inner_html()
                raw_posts.append(html)
            except Exception as e:
                print("Error extracting post HTML:", e)

        print(f"✅ Successfully extracted {len(raw_posts)} raw post HTML blocks")

        # Save to file
        with open("linkedin_group_raw_posts.json", "w", encoding="utf-8") as f:
            json.dump(raw_posts, f, indent=2, ensure_ascii=False)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_group())
