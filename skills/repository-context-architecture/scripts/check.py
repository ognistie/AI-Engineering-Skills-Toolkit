"""Check repository-relative document links, canonical ownership and revision markers."""
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
from _contract import bounded_read, contained, digest, main, sequence, string

LINK = re.compile(
    r"""\]\(\s*(?:<(?P<angle>[^<>\r\n]+)>|(?P<plain>[^()<>\s]+))"""
    r"""(?:\s+(?:"[^"]*"|'[^']*'|\([^()]*\)))?\s*\)"""
)
FENCE = re.compile(r"^ {0,3}(\x60{3,}|~{3,})(.*)$")


def link_targets(text):
    lines, fence = [], None
    for line in text.splitlines():
        marker = FENCE.match(line)
        if fence is not None:
            if (marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence)
                    and not marker[2].strip()):
                fence = None
            continue
        if marker:
            yield from scan_links(lines)
            lines = []
            fence = marker[1]
        else:
            lines.append(line)
    yield from scan_links(lines)


def scan_links(lines):
    for match in LINK.finditer("\n".join(lines)):
        yield match["angle"] or match["plain"]


def analyze(doc):
    root = Path(doc["root"]).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Root must be a directory")
    revision = string(doc["revision"], "revision")
    topics, hashes, findings, seen = {}, {}, [], set()
    for row in sequence(doc["documents"], "documents", 256):
        rel, topic = row["path"], string(row["topic"], "topic")
        path = contained(root, rel)
        if path in seen:
            raise ValueError("Duplicate document in inventory")
        seen.add(path)
        prior = topics.setdefault(topic, rel)
        if prior != rel:
            findings.append(["canonical_conflict", rel, prior])
        if not path.is_file():
            findings.append(["missing_document", rel])
            continue
        data = bounded_read(path)
        other = hashes.setdefault(digest(data), rel)
        if other != rel:
            findings.append(["duplicate_content", rel, other])
        if row.get("observed_revision", revision) != revision:
            findings.append(["revision_mismatch", rel])
        for link in link_targets(data.decode("utf-8")):
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = (path.parent / unquote(parsed.path)).resolve()
            if not target.is_relative_to(root):
                findings.append(["link_outside_repository", rel, link])
            elif not target.exists():
                findings.append(["broken_link", rel, link])
    return {"findings": findings, "documents": len(seen), "checks_semantic_conflicts": False}


if __name__ == "__main__":
    main(analyze, __doc__)
