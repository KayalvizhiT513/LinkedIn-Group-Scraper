import asyncio
import json
from playwright.async_api import async_playwright

LOGIN_STATE = "linkedin_login.json"
GROUP_URL = "https://www.linkedin.com/groups/10155242"

async def scrape_group():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50)
        context = await browser.new_context(storage_state=LOGIN_STATE)
        page = await context.new_page()

        print("Navigating to group...")
        await page.goto(GROUP_URL, timeout=120000, wait_until="domcontentloaded")

        print("Scrolling...")
        for _ in range(15):
            await page.mouse.wheel(0, 3000)
            await asyncio.sleep(2)

        print("Expanding posts...")
        see_more_buttons = await page.locator('button:has-text("…see more")').all()
        for button in see_more_buttons:
            try:
                await button.click()
                await asyncio.sleep(0.5)
            except:
                pass

        print("Extracting posts...")
        posts = []

        post_elements = await page.locator('div.feed-shared-update-v2').all()
        print(f"Found {len(post_elements)} posts")

        for post in post_elements:
            # Extract author
            author = "Unknown"
            try:
                author = await post.locator('span.feed-shared-actor__name').inner_text()
            except:
                try:
                    author = await post.locator('span.update-components-actor__name').inner_text()
                except:
                    pass

            # Extract post content
            content = ""
            try:
                content = await post.locator('span.break-words').inner_text()
            except:
                try:
                    content = await post.locator('div.feed-shared-text').inner_text()
                except:
                    pass

            # If completely empty, skip
            if author == "Unknown" and content.strip() == "":
                continue

            posts.append({
                "author": author.strip(),
                "content": content.strip()
            })

        print(f"✅ Successfully extracted {len(posts)} clean posts")

        with open("linkedin_group_posts.json", "w", encoding="utf-8") as f:
            json.dump(posts, f, indent=4, ensure_ascii=False)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_group())
