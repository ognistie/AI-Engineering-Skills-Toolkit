"""Lint tool discovery, a documented flat schema profile, and recovery errors."""
from math import isfinite
import re
from _contract import canonical, main, sequence, string, strings

TYPES = {"string":str, "boolean":bool, "integer":int, "number":(int,float), "null":type(None)}


def matches(kind, value):
    if kind == "integer":
        return type(value) is int or type(value) is float and isfinite(value) and value.is_integer()
    if kind == "number":
        return type(value) is int or type(value) is float and isfinite(value)
    return type(value) is TYPES[kind]


def enum_key(kind, value):
    return value if kind in ("integer", "number") else canonical(value)


def analyze(doc):
    tools, seen, findings, schemas = sequence(doc["tools"], "tools"), set(), [], {}
    for row in tools:
        name = string(row["name"], "tool name")
        def finding(code, field=""):
            findings.append({"tool": name, "code": code, "field": field})
        start = len(findings)
        if name in seen:
            finding("duplicate_tool")
            schemas.pop(name, None)
        seen.add(name)
        if not re.fullmatch(r"[a-z][a-z0-9_-]*(?:[.:][a-z][a-z0-9_-]*)*", name):
            finding("ambiguous_tool_name")
        if type(row.get("description")) is not str or not row["description"].strip():
            finding("missing_description")
        schema = row["schema"]
        if schema.get("type") != "object" or not isinstance(schema.get("properties"), dict):
            finding("invalid_object_schema")
            continue
        if set(schema) - {"type", "properties", "required", "additionalProperties", "description"}:
            finding("unsupported_schema_keyword")
        properties = schema["properties"]
        for key in strings(schema.get("required", []), "required field"):
            if key not in properties:
                finding("required_field_missing_definition", key)
        if schema.get("additionalProperties") is not False:
            finding("extra_arguments_allowed")
        for key, definition in properties.items():
            kind = definition.get("type")
            if kind not in TYPES or set(definition) - {"type", "enum", "description"}:
                finding("unsupported_schema_keyword_or_type", key)
            elif "enum" in definition:
                choices = sequence(definition["enum"], "enum")
                if (not choices or any(not matches(kind, v) for v in choices)
                        or len({enum_key(kind, v) for v in choices}) != len(choices)):
                    finding("invalid_enum", key)
        if len(findings) == start:
            schemas[name] = schema
        errors = sequence(row.get("errors", []), "errors")
        codes = [err.get("code") for err in errors]
        if (not errors or any(type(code) is not str or not code.strip() for code in codes)
                or len(set(codes)) != len(codes)
                or any(type(err.get("action")) is not str or not err["action"].strip() for err in errors)):
            finding("unactionable_error_contract")
    calls = []
    for row in sequence(doc.get("calls", []), "calls"):
        key = string(row["id"], "call ID")
        schema = schemas.get(row["tool"])
        args = row["arguments"]
        errors = []
        if schema is None or not isinstance(args, dict):
            errors.append("unusable_schema_or_arguments")
        else:
            properties = schema["properties"]
            errors += [f"missing:{name}" for name in sorted(set(schema.get("required", [])) - args.keys())]
            errors += [f"unknown:{name}" for name in sorted(args.keys() - properties.keys())]
            for name in sorted(args.keys() & properties.keys()):
                prop = properties[name]
                kind = prop["type"]
                value = args[name]
                if not matches(kind, value):
                    errors.append(f"wrong_type:{name}")
                elif "enum" in prop and enum_key(kind, value) not in {enum_key(kind, item) for item in prop["enum"]}:
                    errors.append(f"invalid_enum:{name}")
        calls.append({"id":key,"valid":not errors,"errors":errors})
    strings([row["id"] for row in calls], "call ID")
    return {"findings": findings, "catalog_bytes": len(canonical(tools)), "tools": len(tools), "calls":calls}


if __name__ == "__main__":
    main(analyze, __doc__)
