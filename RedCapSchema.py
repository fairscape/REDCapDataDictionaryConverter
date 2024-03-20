from typing import Optional, List
from pydantic import BaseModel, Field

class DataDictionaryItem(BaseModel):
    field_name: str
    field_type: str
    description: str

class RedCapSchema(BaseModel):
    metadataType: str = Field(
        title="metadataType",
        alias="@type",
        default = 'EVI:Schema'
    )
    name: str = Field(max_length=200)
    description: str = Field(min_length=5)
    properties: Optional[List[DataDictionaryItem]] = []

    def parse_schema_csv(self, file_path: str) -> None:
        """Function to load schema file"""
        pass

# Example usage
redcap_schema = RedCapSchema(
    name="Example Schema",
    description="Sample Schema for PreMO RedCapDB."
)
print(redcap_schema.model_dump_json(by_alias=True, indent=2))
