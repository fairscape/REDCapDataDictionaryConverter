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

class DataProperty(BaseModel):
    """Represents a single variable in a RedCap data dictionary."""
    type: str
    description: str
    index: int
    pattern: Optional[str] = None
    minimum: Optional[float] = None
    maximum: Optional[float] = None

class RedCapSchema(BaseModel):
    """Represents a schema for a RedCap database, which can be converted to JSON-LD."""
    context: Dict[str, str] = Field(default=default_context, title="context", alias="@context")
    metadataType: str = Field(title="metadataType", alias="@type", default='EVI:Schema')
    name: str = Field(max_length=200)
    description: str = Field(min_length=4)
    properties: Optional[Dict[str, DataProperty]] = {}
    type: Optional[str] = Field(default="object")
    additionalProperties: Optional[bool] = Field(default=True)
    required: Optional[List[str]] = []  
    separator: Optional[str] = Field(default=",")
    header: Optional[bool] = Field(default=True)
    examples: Optional[List[Dict]] = []  

    @staticmethod
    def generate_regex_from_string(input_string: str) -> str:
        """Converts RedCap radio display rules to a regex pattern."""
        options = [option.strip() for option in input_string.split("|")]
        text_options = [re.escape(option.split(",")[1].strip()) for option in options]
        pattern = f"^({'|'.join(text_options)})$"
        return pattern

    def parse_schema_csv(self, file_path: str, use_numeric_values: bool = False) -> None:
        """Parses a RedCap data dictionary CSV file to populate the schema properties."""
        try:
            df = pd.read_csv(file_path)
        except FileNotFoundError:
            raise Exception(f"File {file_path} not found.")
        except pd.errors.ParserError:
            raise Exception(f"Error parsing CSV file {file_path}.")

        #For every row in the df create a key:value pair describing that property
        self.properties = {
            row['Variable / Field Name']: self._create_data_property(row, index, use_numeric_values)
            for index, row in df.iterrows()
        }

    def _create_data_property(self, row: pd.Series, index: int, use_numeric_values: bool) -> DataProperty:
        """Creates a DataProperty from a row of the CSV file."""
        var = row['Variable / Field Name']
        form_name = row['Form Name']
        description = row['Field Label']
        # Check if description is missing
        if pd.isna(description) or description.strip() == '':
            description = var + " " + form_name
        var_type = row['Field Type']
        type_details = row['Text Validation Type OR Show Slider Number']
        choices = row['Choices, Calculations, OR Slider Labels']

        field_type, pattern = self._determine_field_type_and_pattern(
            var_type, type_details, choices, use_numeric_values
        )

        minimum = row['Text Validation Min'] if not np.isnan(row['Text Validation Min']) else None
        maximum = row['Text Validation Max'] if not np.isnan(row['Text Validation Max']) else None

        return DataProperty(
            type=field_type,
            description=description,
            index=index,
            pattern=pattern,
            minimum=minimum,
            maximum=maximum
        )

    def _determine_field_type_and_pattern(self, var_type: str, type_details: str, choices: str, use_numeric_values: bool) -> (str, Optional[str]):
        """Determines the field type and pattern for a variable based on its RedCap type and details."""
        pattern = None

        if var_type == 'yesno':
            field_type = 'boolean'
        elif type_details == 'integer':
            field_type = 'integer'
        elif type_details == 'number':
            field_type = 'number'
        elif var_type in ['radio', 'dropdown']:
            field_type = 'integer' if use_numeric_values else 'string'
            if not use_numeric_values:
                pattern = self.generate_regex_from_string(choices)
        else:
            field_type = 'string'

        return field_type, pattern


    def save_to_json(self, output_file: str) -> None:
        """Function to save the schema to a JSON file"""
        with open(output_file, 'w') as json_file:
            json.dump(self.model_dump(by_alias=True, exclude_none=True), json_file, indent=4)