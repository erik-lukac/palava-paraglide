import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# Fetch the HTML content
url = 'https://www.pgpalava.cz/homepage/reservations'
response = requests.get(url)
html_content = response.content

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

def get_reservation_count():
    # Find the table or elements that contain the reservation data
    reservation_table = soup.find('table')  # Adjust this selector based on actual HTML structure

    # Initialize a dictionary to store reservation data
    reservation_data = {
        'Den': 'dnes',
        'Datum': '',
        'reservation_count': 0
    }

    if reservation_table:
        # Find all rows in the table
        rows = reservation_table.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            if len(columns) >= 3:
                day = columns[0].get_text(strip=True)
                date = columns[1].get_text(strip=True)
                count = columns[2].get_text(strip=True)

                # Check if the row corresponds to "Dnes" (Today)
                if day.lower() == 'dnes':
                    reservation_data['Datum'] = date
                    try:
                        reservation_data['reservation_count'] = int(count)
                    except ValueError:
                        reservation_data['reservation_count'] = 0
                    break

    return json.dumps(reservation_data)

# Example usage
if __name__ == "__main__":
    print(get_reservation_count())
