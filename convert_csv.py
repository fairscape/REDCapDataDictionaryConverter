from RedCapSchema import *

redcap_schema = RedCapSchema(
    name="Schema Name",
    description="Sample description for schema."
)

redcap_schema.parse_schema_csv('/path/to/red_cap_schema.csv')
redcap_schema.save_to_json('/output/path/converted_schema.json')
