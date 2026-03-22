from Repositories.BirdsApiConnector import BirdsApiConnector
import datetime
from typing import Optional

class BirdsApiService:
    
    def __init__(self):
        self.connector = BirdsApiConnector() 
        # TODO: Make host url being read from .env
    
    def get_species(self):
        species_df = self.connector.get_table(table_name="species")
        
        return species_df
    
    def add_species(self, name:str, scientific_name:str, family:str, conservation_status:str, wingspan_cm:float):
        self.connector.add_element(
            table_name="species",
            payload={
                "name": name,
                "scientific_name": scientific_name,
                "family": family,
                "conservation_status": conservation_status,
                "wingspan_cm": wingspan_cm
            })
    
    def get_birds(self):
        birds_df = self.connector.get_table(table_name="birds")
        species_df = self.connector.get_table(table_name="species")
        
        birds_df = (
            birds_df
            .merge(species_df, left_on='species_id', right_on='id', how='left', suffixes=('', '_species'))
            .drop(columns=['species_id', 'id_species'])
            .rename(columns={'name': 'species_name'})
        )
        
        return birds_df
    
    def add_birds(self, species_id:int, nickname:str, ring_code:str, age:int):
        self.connector.add_element(
            table_name="species",
            payload={
                "species_id": species_id,
                "nickname": nickname,
                "ring_code": ring_code,
                "age": age
            })
        
    def get_bird_spotting(self):
        spotting_df = self.connector.get_table(table_name="bird_spotting")
        birds_df = self.get_birds()

        return (
            spotting_df
            .merge(birds_df, left_on='bird_id', right_on='id', how='left', suffixes=('', '_bird'))
            .drop(columns=['bird_id', 'id_bird'])
        )
    
    def add_bird_spotting(self, bird_id: int, spotted_at: datetime, location: str, observer_name: str, notes: Optional[str] = None):
        self.connector.add_element(
            table_name="bird_spotting",
            payload={
                "bird_id": bird_id,
                "spotted_at": spotted_at.isoformat(),
                "location": location,
                "observer_name": observer_name,
                "notes": notes
            })
    
if __name__ == "__main__":
    api_service = BirdsApiService()
    birds_df = api_service.get_bird_spotting()
    print(birds_df.head())