"""Check an offline claim-to-source ledger; never fetch or authenticate evidence."""
import argparse
import json
from pathlib import Path


def unique_by_id(rows, name):
    if not isinstance(rows, list) or not rows:
        raise ValueError(f"{name} must be a nonempty list")
    result = {}
    for row in rows:
        key = row["id"]
        if type(key) is not str or not key.strip() or key in result:
            raise ValueError(f"Invalid or duplicate {name} ID")
        result[key] = row
    return result


def validate(document):
    sources = unique_by_id(document["sources"], "source")
    claims = unique_by_id(document["claims"], "claim")
    locators = {}
    for row in sources.values():
        locator, group = row["locator"], row["group"]
        if any(type(value) is not str or not value.strip() for value in (locator, group)):
            raise ValueError("Source locator and evidence group are required")
        locator, group = locator.strip(), group.strip()
        if locators.setdefault(locator, group) != group:
            raise ValueError("Identical source locator assigned to multiple evidence groups")

    output = {}
    for key, claim in claims.items():
        if type(claim["statement"]) is not str or not claim["statement"].strip():
            raise ValueError("Empty claim")
        items = claim["evidence"]
        if not isinstance(items, list):
            raise ValueError("Evidence must be a list")
        support, contrary, seen = set(), set(), set()
        for item in items:
            source_id, stance = item["source"], item["stance"]
            if source_id not in sources or stance not in ("supports", "contradicts", "neutral"):
                raise ValueError(f"{key}: unknown source or stance")
            if (source_id, stance) in seen:
                raise ValueError(f"{key}: repeated evidence citation")
            seen.add((source_id, stance))
            group = sources[source_id]["group"].strip()
            if stance == "supports":
                support.add(group)
            elif stance == "contradicts":
                contrary.add(group)
        state = ("mixed" if support and contrary else "contrary_only" if contrary else
                 "multiple_groups" if len(support) > 1 else "single_group" if support else "unsubstantiated")
        output[key] = {"status": state, "support_groups": sorted(support), "contrary_groups": sorted(contrary)}
    return {"claims": output, "source_authenticity": "not_verified"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    args = parser.parse_args()
    try:
        with args.ledger.open("rb") as stream:
            data = stream.read(2_000_001)
        if len(data) > 2_000_000:
            raise ValueError("Input exceeds 2 MB")
        print(json.dumps(validate(json.loads(data, object_pairs_hook=unique_pairs)), indent=2))
    except (OSError, ValueError, TypeError, KeyError, RecursionError) as exc:
        parser.exit(2, f"Invalid ledger: {exc}\n")


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


if __name__ == "__main__":
    main()
