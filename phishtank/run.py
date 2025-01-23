import asyncio
import json

from bs4 import BeautifulSoup
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

BASE_URL = "https://phishtank.org/stats/{year}/{month}/"

YEARS = range(2009, 2025)
MONTHS = [
    "01",
    "02",
    "03",
    "04",
    "05",
    "06",
    "07",
    "08",
    "09",
    "10",
    "11",
    "12",
]

URLS = [BASE_URL.format(year=year, month=month) for year in YEARS for month in MONTHS]


async def extract_stats(html_content, url):
    # Convert string to BeautifulSoup object
    soup = BeautifulSoup(html_content, "html.parser")
    stats = {}
    for h3 in soup.find_all("h3"):
        title = h3.text.split(":")[0].strip()
        if title in [
            "Total Submissions",
            "Valid Phishes",
            "Invalid Phishes",
            "Total Votes",
            "Median Time To Verify",
        ]:
            value = h3.find("b").text.strip() if h3.find("b") else None
            if title not in stats:
                stats[title] = {}
            # Extract year and month from current URL
            url_parts = url.split("/")
            year = url_parts[-3]
            month = url_parts[-2]
            if year not in stats[title]:
                stats[title][year] = {}
            stats[title][year][month] = value
    return stats


async def main():
    final_stats = {
        "Total Submissions": {},
        "Valid Phishes": {},
        "Invalid Phishes": {},
        "Total Votes": {},
        "Median Time To Verify": {},
    }

    async with AsyncWebCrawler() as crawler:
        for url in URLS:
            result = await crawler.arun(
                url=url,
                config=CrawlerRunConfig(
                    css_selector=".padded", exclude_external_links=True
                ),
            )
            if result.success:
                year = url.split("/")[-3]
                month = url.split("/")[-2]
                stats = await extract_stats(result.cleaned_html, url)

                # Update final_stats with the results
                for stat_type, values in stats.items():
                    if year not in final_stats[stat_type]:
                        final_stats[stat_type][year] = {}
                    final_stats[stat_type][year][month] = values

                print(f"Processed {url}")
            else:
                print(f"Failed to process {url}")

    # Save to JSON file
    with open("phishtank_stats.json", "w", encoding="utf-8") as f:
        json.dump(final_stats, f, indent=2)
    print("Results saved to phishtank_stats.json")


if __name__ == "__main__":
    asyncio.run(main())
