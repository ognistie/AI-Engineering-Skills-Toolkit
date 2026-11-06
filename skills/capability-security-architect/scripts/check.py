"""Check exact scope attenuation for trusted capability descriptors."""
from _contract import integer, main, string, strings

DIMENSIONS = ("tools","resources","effects")


def grant(item):
    subject = string(item["subject"], "subject")
    scope = {key:set(strings(item[key], key)) for key in DIMENSIONS}
    if any(not value for value in scope.values()) or not scope["effects"] <= {"read","write","external","destructive"}:
        raise ValueError("Expected nonempty exact scopes and recognized effects")
    if any("*" in value or "?" in value for values in scope.values() for value in values):
        raise ValueError("Wildcard grants are unsupported")
    if type(item["delegable"]) is not bool:
        raise ValueError("Delegability must be boolean")
    return subject, scope, integer(item["expires"], "expiry"), item["delegable"]


def analyze(doc):
    now = integer(doc["now"], "trusted clock")
    parent, parent_scope, expiry, delegable = grant(doc["parent"])
    child, scope, child_expiry, child_delegable = grant(doc["child"])
    if doc["child"]["issuer"] != parent or not delegable:
        return {"decision":"deny","reason":"delegation_not_authorized"}
    if now >= expiry or now >= child_expiry or child_expiry > expiry:
        return {"decision":"deny","reason":"expiry"}
    if any(not scope[k] <= parent_scope[k] for k in DIMENSIONS):
        return {"decision":"deny","reason":"scope_expansion"}
    if "request" in doc:
        action = doc["request"]
        attrs = {"tools":"tool","resources":"resource","effects":"effect"}
        if action["subject"] != child or any(action[field] not in scope[dim] for dim,field in attrs.items()):
            return {"decision":"deny","reason":"request_outside_grant"}
    return {"decision":"allow","reason":"attenuated","issued":False,
            "child_may_delegate":child_delegable}


if __name__ == "__main__":
    main(analyze, __doc__)
