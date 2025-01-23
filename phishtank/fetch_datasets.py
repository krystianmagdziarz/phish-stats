import asyncio
import json
import aiohttp
from bs4 import BeautifulSoup
import os

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


async def fetch_url(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


async def main():
    final_stats = {
        "Total Submissions": {},
        "Valid Phishes": {},
        "Invalid Phishes": {},
        "Total Votes": {},
        "Median Time To Verify": {},
    }

    async with aiohttp.ClientSession() as session:
        for url in URLS:
            html_content = await fetch_url(session, url)
            if html_content:
                year = url.split("/")[-3]
                month = url.split("/")[-2]
                stats = await extract_stats(html_content, url)

                # Update final_stats with the results
                for stat_type, values in stats.items():
                    if year not in final_stats[stat_type]:
                        final_stats[stat_type][year] = {}
                    final_stats[stat_type][year][month] = values[year][month]

                print(f"Processed {url}")
            else:
                print(f"Failed to process {url}")

    # Create datasets directory if it doesn't exist
    os.makedirs("datasets", exist_ok=True)

    # Save to JSON file in datasets folder
    with open("datasets/phishtank_stats.json", "w", encoding="utf-8") as f:
        json.dump(final_stats, f, indent=2)
    print("Results saved to datasets/phishtank_stats.json")


if __name__ == "__main__":
    asyncio.run(main())
