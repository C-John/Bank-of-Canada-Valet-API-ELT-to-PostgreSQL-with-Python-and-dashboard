import requests

def discover_groups():
    
    # Use one of the IDs you found in the last 
    data = requests.get("https://www.bankofcanada.ca/valet/observations/group/FX_RATES_DAILY/json").json()

    for series_id in list(data['seriesDetail'].keys()):
                
        url = f"https://www.bankofcanada.ca/valet/observations/{series_id}/json"

        # 1. Fetch the actual data
        response = requests.get(url)
        data = response.json()

        # 2. Get the list of observations (The dates and values)
        observations = data['observations']
        print(data['observations'])
        total_rows = len(observations)

        print(f"Total rows found for {series_id}: {total_rows}")

    # index = 0
    # # 3. Print the first 10 rows to see the numbers
    # while index < 10:
    #     row = observations[index]
    #     # 'd' is the date, the series_id is the value
    #     date = row['d']
    #     value = row[series_id]['v']
        
    #     print(f"Date: {date} | Value: {value}")
    #     index += 1
           
    # # 1. Get the list of all individual SERIES (this is the big 10k+ list)
    # data = requests.get("https://www.bankofcanada.ca/valet/observations/group/FX_RATES_DAILY/json").json()
    # series_keys = list(data['seriesDetail'].keys())

    # index = 0
    # total_series = len(series_keys)

    # print(f"Total individual series found: {total_series}")

    # # 2. Eyeball the first 20 series
    # while index < 20:
    #     s_id = series_keys[index]
    #     label = data['seriesDetail'][s_id]['label']
        
    #     print(f"[{index}] Series ID: {s_id} | Name: {label}")
        
    #     index += 1
        
    # url = "https://www.bankofcanada.ca/valet/lists/groups/json"
    # response = requests.get(url)
    # # print(response.text)
    # data = response.json()
    # # print(data)

    # # 1. Get the keys as a list so we can use a number to track our position
    # group_ids = list(data['groups'].keys())

    # # 2. Set our starting position
    # index = 0

    # # 3. Loop as long as the index is less than the total number of items
    # while index < len(group_ids):
    #     # Get the ID using the current index
    #     current_id = group_ids[index]
        
    #     # Get the details using that ID
    #     details = data['groups'][group_ids[index]]
        
    #     print(f"{current_id}: {details['label']}")
        
    #     # 4. CRITICAL: Manually move to the next item
    #     index += 1

if __name__ == "__main__":
    discover_groups()