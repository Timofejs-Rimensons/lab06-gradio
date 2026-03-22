import requests
import pandas as pd
import json

class BirdsApiConnector:
    def __init__(self, host_url="http://localhost:8000"):
        self.host_url = host_url
        
    def get_table(self, table_name):
        response = requests.get(f"{self.host_url}/{table_name}")
        response.raise_for_status()
        df = pd.DataFrame.from_dict(response.json())
        return df
    
    def add_element(self, table_name, payload):
        response = requests.post(
            f"{self.host_url}/{table_name}/",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
