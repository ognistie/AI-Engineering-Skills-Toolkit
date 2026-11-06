"""Select visible tool contracts by host-classified intent within a byte budget."""
from _contract import canonical, integer, main, sequence, string, strings


def analyze(doc):
    intent = string(doc["intent"], "intent")
    allowed = set(strings(doc["allowed"], "allowed tool"))
    maximum = integer(doc["max_tools"], "tool limit", 1)
    budget = integer(doc["max_bytes"], "byte limit")
    tools = sequence(doc["catalog"], "catalog")
    identifiers = set(strings([row["id"] for row in tools], "tool ID"))
    if not allowed <= identifiers:
        raise ValueError("Allowed tool is not in the trusted catalog")
    matching = []
    for tool in tools:
        intents = strings(tool["intents"], "intent")
        if not isinstance(tool["schema"], dict):
            raise ValueError("Expected tool schema object")
        if tool["id"] in allowed and intent in intents:
            visible = {"id":tool["id"],"schema":tool["schema"]}
            matching.append((len(canonical(visible)), tool["id"], visible))
    selected, skipped = [], []
    for _, identifier, visible in sorted(matching):
        if len(selected) < maximum and len(canonical(selected+[visible])) <= budget:
            selected.append(visible)
        else:
            skipped.append(identifier)
    return {"decision":"shortlist" if selected else "abstain","selected":selected,
            "exposure_bytes":len(canonical(selected)) if selected else 0,
            "eligible_but_not_exposed":skipped,"token_cost_measured":False}


if __name__ == "__main__":
    main(analyze, __doc__)
