# REDCap to JSON-LD Converter

This repository contains code that converts a REDCap data dictionary CSV into JSON-LD metadata, adhering to the specifications outlined [here](https://fairscape.github.io/fairscape-cli/schema-metadata/). For instructions on how to export your data dictionary from REDCap, please refer to [this guide](https://redcap.smhs.gwu.edu/sites/g/files/zaskib651/files/2021-07/Download%20the%20Data%20Dictionary.pdf).


## Example Usage

The following example demonstrates how to use the RedCapSchema class to convert a REDCap data dictionary CSV into a JSON-LD schema:
```python
from RedCapSchema import *

# Initialize the RedCapSchema object with a name and description
redcap_schema = RedCapSchema(
    name="Schema Name",
    description="Sample description for schema."
)

# Parse the REDCap data dictionary CSV
redcap_schema.parse_schema_csv('/path/to/red_cap_schema.csv')

# Save the converted schema as JSON-LD
redcap_schema.save_to_json('/output/path/converted_schema.json')
```

In this example, we first import the RedCapSchema class. We then create an instance of RedCapSchema by providing a schema name and description. The parse_schema_csv method is used to read and parse the REDCap data dictionary CSV file. Finally, the save_to_json method saves the converted schema in JSON-LD format to the specified output path.

## Contribution

If you'd like to request a feature or report a bug, please create a [GitHub Issue](https://github.com/fairscape/RedCapSchema/issues) using one of the templates provided.


## License

This project is licensed under the terms of the MIT license.