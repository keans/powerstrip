# cerberus schema for plugin metadata
plugin_metadata_schema = {
    "uuid": {
        "type": "string",
        "required": True,
        "check_with": "is_hex"
    },
    "name": {
        "type": "string",
        "required": True,
        "check_with": "is_alphanumeric"
    },
    "description": {
        "type": "string",
        "required": True,
    },
    "version": {
        "type": "string",
        "required": True,
        "check_with": "is_semver"
    },
    "url": {
        "type": "string",
        "required": True,
        "check_with": "is_url"
    },
}
