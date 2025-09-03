# pip install playwright pandas
# python -m playwright install

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from urllib.parse import quote_plus
import pandas as pd

def web_scraper(query: str, max_results, scrolls):
    results = []
    

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
    
       
        context = browser.new_context(viewport={"width": 1366, "height": 768})
        page = context.new_page()

        # Open search page
        page.goto(f"https://www.youtube.com/results?search_query={quote_plus(query)}", wait_until="domcontentloaded")

        # Click the "Videos" tab if present
        try:
            page.locator('xpath=//yt-chip-cloud-chip-renderer//div[normalize-space()="Videos"]').first.click()
            page.wait_for_selector("ytd-video-renderer", timeout=10000)
        except PlaywrightTimeoutError:
            # Videos chip not found quickly — continue with default results
            pass
        except Exception:
            pass

        # Limited scrolling (like your for-range loop)
        for _ in range(scrolls):
            page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight);")
            page.wait_for_timeout(1500)  # small pause so more results render

        # Iterate sections, then videos (mirrors your structure)
        sections = page.locator("ytd-item-section-renderer")
        for si in range(sections.count()):
            section = sections.nth(si)
            videos = section.locator("ytd-video-renderer")

            for vi in range(videos.count()):
                if len(results) >= max_results:
                    break

                v = videos.nth(vi)
                try:
                    # Title + href from #video-title
                    title_el = v.locator("#video-title").first
                    # Some results only expose 'title' attr; others have text
                    title = (title_el.get_attribute("title") or title_el.inner_text()).strip()
                    href = title_el.get_attribute("href")
                    if not href:
                        continue
                    if href.startswith("/"):
                        href = "https://www.youtube.com" + href

                    # Description (optional)
                    desc_el = v.locator("yt-formatted-string.metadata-snippet-text").first
                    try:
                        description = desc_el.inner_text().strip()
                    except Exception:
                        description = None

                    results.append({
                        "title": title,
                        "link": href,
                        "description": description
                    })
                except Exception:
                    # Skip cards/ads/special renderers
                    continue

            if len(results) >= max_results:
                break

        browser.close()

    # Optional: drop duplicate links and trim to max_results
    df = pd.DataFrame(results)
    if not df.empty:
        df = df.drop_duplicates(subset="link", keep="first").head(max_results)
    return df

def main():
    import os
    path_name = "youtube-python-scrapping"
    folder = os.listdir(path_name)
    print(f"Running from folder: {folder}")
    with open('youtube_scraper.py', 'r') as g:
        content = g.read()
        
        
        
    for file in folder:
         if file == "youtube_scraper.py":
           print(f"writing file: {file}")
           target_path = os.path.join(path_name, file)
           with open(target_path, 'w') as f:
               f.open(target_path, 'w').write(content)
               
               print(f)
               
               
    # print(f"Running from: {dir}")
    # dir_name = "/youtube-python-scrapping"
    # for dir in 
# Example

# df = web_scraper("farming technology", max_results=100, scrolls=4)
# print(len(set(df['description'].unique())))
main()