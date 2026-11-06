"""Validate a whole plan before invoking any trusted tool callbacks."""
from _contract import main, sequence, string, strings


def dispatch(plan, permissions, handlers, policy=None):
    actions = sequence(plan, "plan", 128)
    strings([row["id"] for row in actions], "action ID")
    scopes = {string(tool, "trusted tool"):set(strings(resources, "resource")) for tool,resources in permissions.items()}
    # Freeze validated fields so callbacks cannot mutate the caller's original plan after preflight.
    validated = []
    for row in actions:
        if set(row) != {"id","tool","resource"}:
            return {"decision":"deny","reason":"proposal_schema","id":row["id"],"receipts":[]}
        tool = string(row["tool"], "tool")
        resource = string(row["resource"], "resource")
        if tool not in handlers or resource not in scopes.get(tool, set()):
            return {"decision":"deny","reason":"outside_trusted_scope","id":row["id"],"receipts":[]}
        action = (row["id"], tool, resource, handlers[tool])
        if policy is not None and policy(row["id"], tool, resource) is not True:
            return {"decision":"deny","reason":"external_policy","id":row["id"],"receipts":[]}
        validated.append(action)
    receipts = []
    for key, tool, resource, handler in validated:
        receipts.append({"id":key,"tool":tool,"result":handler(resource)})
    return {"decision":"dispatched","receipts":receipts}


def analyze(doc):
    permissions = doc["trusted_permissions"]
    fake = {name:lambda resource:{"simulated":True,"resource":resource} for name in permissions}
    return dispatch(doc["plan"], permissions, fake) | {"environment":"inert_local_demo"}


if __name__ == "__main__":
    main(analyze, __doc__)
