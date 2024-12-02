import requests
import pandas as pd

api_url = "http://127.0.0.1:8000"

vehicle_endpoint = f"{api_url}/vehicles"
location_endpoint = f"{api_url}/locations"
headers = {
    "Content-Type": "application/json",
    # "Authorization": "Bearer your_token_here"  # Add if authentication is required
}
file_path = "C:/Users/kiran/Downloads/locations_vehicles_data.xlsx"

excel_data = pd.ExcelFile(file_path)

location_df = pd.read_excel(excel_data,sheet_name="Locations")
vehicles_df = pd.read_excel(excel_data,sheet_name="Vehicles")

location_df = location_df.where(pd.notnull(location_df),None)
vehicles_df = vehicles_df.where(pd.notnull(vehicles_df),None)
def post_data(row,endpoint):
    if not isinstance(row, dict):
        row = row.to_dict()
    try:
        response = requests.post(endpoint,headers=headers,json=row)
        response.raise_for_status()
        print(f"Success: {row}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {row} - {e}")
        print("Response content:", response.content) 

def create_data():
    for data,location in location_df.iterrows():
        location_data = location.to_dict()
        post_data(location_data,location_endpoint) 

    for data,vehicle in vehicles_df.iterrows():
        vehicle_data = vehicle.to_dict()
        post_data(vehicle_data,vehicle_endpoint)

     

create_data()
