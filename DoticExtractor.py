import asyncio  
import httpx  
from bs4 import BeautifulSoup  
import csv  
import re  

input_file = "urls.txt"  
output_file = "scraped_data.csv"  

async def scrape_url(client, url, writer, cookies):  
    print(f"Scraping: {url}")  
    try:  
        response = await client.get(url, cookies=cookies)  
        if response.status_code != 200:  
            print(f"Failed to scrape {url} (Status: {response.status_code})")  
            return  

        soup = BeautifulSoup(response.text, "html.parser")  

        title_tag = soup.find(class_="title")  
        title = " ".join(title_tag.get_text(strip=True).split()) if title_tag else ""  

        text_tag = soup.find(class_="matn")  
        text = " ".join(text_tag.get_text(strip=True).split()) if text_tag else ""  

        pdf_tag = soup.find(class_="pull-left")  
        pattern = r'href=[\'"]?([^\'" >]+)'  
        pdf_link = re.search(pattern, str(pdf_tag))  
        href_value = pdf_link.group(1) if pdf_link else None  

        writer.writerow([title, text, href_value, url])  
        print(f"✅ Scraped successfully: {url}")  

    except Exception as e:  
        print(f"Error scraping {url}: {e}")  

async def main():  
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:  
        writer = csv.writer(file)  
        writer.writerow(["title", "text", "pdf", "url"])  

        async with httpx.AsyncClient() as client:  
            with open(input_file, "r") as f:  
                urls = [line.strip() for line in f.readlines()]  
 
            batch_size = 20  
            for i in range(0, len(urls), batch_size):  
                batch = urls[i:i + batch_size]  
                
                tasks = [scrape_url(client, url, writer, cookies) for url in batch]  
                await asyncio.gather(*tasks)  
  
                if i + batch_size < len(urls):  
                    print(f"Waiting for 3 seconds before processing the next batch...\n")  
                    await asyncio.sleep(3)  

# Cookie configuration  
cookies = {  
    "__arcsjs": "b5ba19b4e1d4a8c355e19cf88c92de50"  
}  
 
if __name__ == "__main__":  
    asyncio.run(main())  
    print("Scraping completed!")