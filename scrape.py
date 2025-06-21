from playwright.sync_api import sync_playwright

def scrape_chapter():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Headless browser (no GUI)
        page = browser.new_page()
        
       
        url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"
        page.goto(url)

        
        page.screenshot(path="chapter_screenshot.png")

        
        content = page.inner_text("div#mw-content-text")

        
        with open("chapter1_text.txt", "w", encoding="utf-8") as f:
            f.write(content)

        print("Scraping done. Screenshot and text saved.")
        browser.close()

if __name__ == "__main__":
    scrape_chapter()
