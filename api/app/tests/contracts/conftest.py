import jsonschema
import pytest


def validate_schema(response_json, schema):
    __tracebackhide__ = True
    try:
        jsonschema.validate(instance=response_json, schema=schema)
    except jsonschema.ValidationError as error:
        path = ".".join(str(part) for part in error.absolute_path)
        location = path or "<root>"
        if error.validator == "required" and error.message.startswith("'"):
            missing_property = error.message.split("'", 2)[1]
            location = f"{path}.{missing_property}" if path else missing_property
        pytest.fail(f"Schema validation failed at {location}: {error.message}")
    except jsonschema.SchemaError as error:
        pytest.fail(f"Invalid schema: {error.message}")
