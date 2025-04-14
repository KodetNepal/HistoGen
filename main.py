import requests
import csv
from tqdm import tqdm
import time
from datetime import datetime

def fetch_historical_events(start_year=1900, end_year=2025, filename='historical_events.csv'):
    """
    Fetch historical events from HistoryLabs API and save to CSV
    Args:
        start_year (int): First year to fetch (default: 1900)
        end_year (int): Last year to fetch (default: 2025)
        filename (str): Output CSV filename
    """
    base_url = "https://events.historylabs.io/year"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['year', 'date', 'event', 'source_url'])

        for year in tqdm(range(start_year, end_year + 1), desc="Fetching historical events"):
            try:
                response = requests.get(f"{base_url}/{year}", headers=headers)
                response.raise_for_status()
                data = response.json()

                source_url = data.get('sourceUrl', '')

                for event in data.get('events', []):
                
                    content = event.get('content', '')
                    event_date = event.get('date', '')

                    if not event_date and '\n' in content:
                        first_line = content.split('\n')[0]
                        try:
                            
                            datetime.strptime(first_line, '%B %d')
                            event_date = f"{year} {first_line}"
                            content = '\n'.join(content.split('\n')[1:]) 
                        except ValueError:
                            pass

                    writer.writerow([
                        year,
                        event_date.strip(),
                        content.strip(),
                        source_url
                    ])

                time.sleep(0.3) 

            except requests.RequestException as e:
                print(f"\nError fetching data for {year}: {e}")
                continue
            except Exception as e:
                print(f"\nError processing {year}: {e}")
                continue

    print(f"\nSuccessfully saved historical events to {filename}")

if __name__ == "__main__":
    fetch_historical_events()  # Full range 1900-2025
    # fetch_historical_events(2020, 2025, 'recent_events.csv')
