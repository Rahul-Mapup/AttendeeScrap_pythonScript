import requests
import csv

def extract_and_write_to_csv(url, headers, params, properties_to_extract, csv_file_path, has_pages=True):
    page = 1
    all_data = []

    while True:
        current_headers = headers.copy()
        current_params = params.copy()
        current_params['page'] = page

        response = requests.get(url, headers=current_headers, params=current_params)
        data = response.json()

        # Break if there is no more data or has_pages is False
        if not data.get("data") or not has_pages:
            break

        all_data.extend(data.get("data"))
        page += 1

    # Extracted properties to be written to CSV
    csv_headers = properties_to_extract
    csv_rows = []

    for item in all_data:
        row_data = [item.get(prop) for prop in properties_to_extract]
        csv_rows.append(row_data)

    # Write to CSV file
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(csv_headers)
        csv_writer.writerows(csv_rows)

    print(f"CSV file '{csv_file_path}' has been successfully created.")

url = "https://api-prod.grip.events/1/container/6559/search"
headers = {
    'authority': 'api-prod.grip.events',
    'accept': 'application/json',
    'accept-language': 'en-gb',
    'cache-control': 'No-Cache',
    'content-type': 'application/json',
    'login-source': 'web',
    'origin': 'https://matchmaking.grip.events',
    'pragma': 'No-Cache',
    'referer': 'https://matchmaking.grip.events/manifestvegas2024/app/home/network/list/68095',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'x-authorization': 'b27cae08-d80c-494d-96fe-8b31c8416542',
    'x-grip-version': 'Web/25.0.7'
}
params = {
    'search': '',
    'sort': 'name',
    'order': 'asc',
    'type_id': '5714,5718,5716,5717,8505'
}
properties_to_extract = ["name", "headline", "summary", "job_title", "location"]
csv_file_path = "attendees_data.csv"

extract_and_write_to_csv(url, headers, params, properties_to_extract, csv_file_path, has_pages=True)

