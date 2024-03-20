from typing import Optional
from pydantic import BaseModel, Field


class RedCapSchema(BaseModel):
    metadataType: str = Field(
        title="metadataType",
        alias="@type",
        default = 'EVI:Schema'
    )
    name: str = Field(max_length=200)
    description: str = Field(min_length=5)
    file_path: str = Field(..., title="File Path", description="Path to the file")

# Example usage
redcap_schema = RedCapSchema(
    name="Example Schema",
    description="Sample Schema for PreMO RedCapDB.",
    file_path="/path/to/file"
)
