import requests as re
import json
import pandas as pd


class Requester:
    
    def __init__(self):
        
        with open("FARS_URLS.json") as f:
            self.fars_urls = json.load(f)
        
    
    def get_fars_data(self, extensionNumber = 1):
        
        # Get the API url by the extension number
        base_url = "https://crashviewer.nhtsa.dot.gov/CrashAPI"        
        endpoint_path = self.fars_urls[str(extensionNumber)]
        api_url = f"{base_url}{endpoint_path}"
        
        # Make a get request to the API and extract json result
        result = re.get(api_url)        
        data = result.json()["Results"][0]

        # Format as pandas DataFrame and save it to data folder
        keys = data[0].keys()
        df = pd.DataFrame({k: [d[k] for d in data] for k in keys})
        df.to_csv(f"../data/fars_data_{extensionNumber:02d}.csv")

    def get_someother_data(self):
        pass
    
    
if __name__ == "__main__":
    dataRequester = Requester()
    
    dataRequester.get_fars_data()
    