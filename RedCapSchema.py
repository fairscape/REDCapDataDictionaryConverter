from typing import Optional, List, Dict
from pydantic import BaseModel, Field
import pandas as pd
import numpy as np
import re
import json

default_context = {
    "@vocab": "https://schema.org/",
    "evi": "https://w3id.org/EVI#"
}
class DataDictionaryItem(BaseModel):
    """Class that holds required information for a redcap variable"""
    field_name: str
    field_type: str
    description: str
    index: int
    pattern: Optional[str] = None
    minimum: Optional[float] = None
    maximum: Optional[float] = None

class RedCapSchema(BaseModel):
    """Class for loading and converting redcap schema to json-ld"""
    context: Dict[str, str] = Field(
        default=default_context,
        title="context",
        alias="@context"
    )
    metadataType: str = Field(
        title="metadataType",
        alias="@type",
        default='EVI:Schema'
    )
    name: str = Field(max_length=200)
    description: str = Field(min_length=5)
    properties: Optional[List[DataDictionaryItem]] = []
    type: Optional[str] = Field(default="object")
    additionalProperties: Optional[bool] = Field(default=True)
    required: Optional[List] = []
    separator: Optional[str] = Field(default=",")
    header: Optional[bool] = Field(default=True)
    examples: Optional[List] = []

    @staticmethod
    def generate_regex_from_string(input_string: str) -> str:
        """Takes redcap rules for radio display and converts to allowed regex"""
        # Split the string into options
        options = input_string.split(" | ")

        # Extract the text portion of each option and escape special characters
        text_options = [re.escape(option.split(", ")[1]) for option in options]

        # Join the options with the pipe operator for the regex pattern
        pattern = f"^({'|'.join(text_options)})$"

        return pattern

    def parse_schema_csv(self, file_path: str, use_numeric_values: bool = False) -> None:
        """Function to parse input csv into properties"""
        df = pd.read_csv(file_path)
        properties = []
        pattern = None
        
        for index, row in df.iterrows():
            var = row['Variable / Field Name']
            description = row['Field Label']
            var_type = row['Field Type']
            type_details = row['Text Validation Type OR Show Slider Number']

            if var_type == 'yesno':
                field_type = 'boolean'
            elif type_details == 'integer':
                field_type = 'integer'
            elif type_details == 'number':
                field_type = 'number'
            elif var_type in ['radio', 'dropdown']:
                if use_numeric_values:
                    field_type = 'integer'
                else:
                    pattern = self.generate_regex_from_string(row['Choices, Calculations, OR Slider Labels'])
                    field_type = 'string'
            else:
                field_type = 'string'

            minimum = row['Text Validation Min'] if not np.isnan(row['Text Validation Min']) else None
            maximum = row['Text Validation Max'] if not np.isnan(row['Text Validation Max']) else None

            properties.append(DataDictionaryItem(
                field_name=var,
                field_type=field_type,
                description=description,
                index=index,
                pattern=pattern,
                minimum=minimum,
                maximum=maximum
            ))

        self.properties = properties

    def save_to_json(self, output_file: str) -> None:
        """Function to save the schema to a JSON file"""
        with open(output_file, 'w') as json_file:
            json.dump(self.model_dump(by_alias=True, exclude_none=True), json_file, indent=4)