"""
parse_cards.py

Parses card data from cards.onj (ONJ is a JSON-like custom config format).

Extracts plain scalar fields: name, title, baseDamage, coverValue, cost,
price, dark, tags, traitEffects, description, flavourText.

Limitations:
  - Fields using ONJ expressions (effects, rotation, passiveEffects) are
    not parsed.
  - Descriptions that use string concatenation (e.g. "text" + slot.3 + "more")
    are truncated to the first string segment only.

Public API
----------
load_cards(path=None) -> list[dict]
    Parse cards.onj and return every card entry as a dict.

get_obtainable_cards(cards=None) -> list[dict]
    Filter out cards tagged 'not used' or 'unobtainable'.
"""

import re
from pathlib import Path
from typing import Optional, Union

_CARDS_ONJ = Path(__file__).parent / "cards.onj"


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _strip_comments(text: str) -> str:
    """Remove // line comments and /* */ block comments."""
    result = []
    i = 0
    while i < len(text):
        if text[i:i+2] == "//":
            while i < len(text) and text[i] != "\n":
                i += 1
        elif text[i:i+2] == "/*":
            i += 2
            while i < len(text) and text[i:i+2] != "*/":
                i += 1
            i += 2
        else:
            result.append(text[i])
            i += 1
    return "".join(result)


def _extract_card_blocks(text: str) -> list:
    """Split the cards: [...] array into individual { } blocks."""
    m = re.search(r"\bcards\s*:\s*\[", text)
    if not m:
        return []

    blocks = []
    i = m.end()
    while i < len(text):
        while i < len(text) and text[i].isspace():
            i += 1
        if i >= len(text) or text[i] == "]":
            break
        if text[i] == "{":
            depth = 0
            start = i
            while i < len(text):
                if text[i] == "{":
                    depth += 1
                elif text[i] == "}":
                    depth -= 1
                    if depth == 0:
                        blocks.append(text[start:i + 1])
                        i += 1
                        break
                i += 1
        else:
            i += 1
    return blocks


def _get_str(block: str, key: str) -> Optional[str]:
    """Return the first quoted string value for key."""
    pat = rf"\b{re.escape(key)}\s*:\s*(?:'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\")"
    m = re.search(pat, block)
    if not m:
        return None
    return m.group(1) if m.group(1) is not None else m.group(2)


def _get_int(block: str, key: str) -> Optional[int]:
    m = re.search(rf"\b{re.escape(key)}\s*:\s*(-?\d+)", block)
    return int(m.group(1)) if m else None


def _get_bool(block: str, key: str) -> Optional[bool]:
    m = re.search(rf"\b{re.escape(key)}\s*:\s*(true|false)", block)
    return (m.group(1) == "true") if m else None


def _get_str_array(block: str, key: str) -> list:
    """Return all quoted strings inside the array value for key."""
    m = re.search(rf"\b{re.escape(key)}\s*:\s*\[(.*?)]", block, re.DOTALL)
    if not m:
        return []
    return [
        g[0] or g[1]
        for g in re.findall(r'"((?:[^"\\]|\\.)*)"|\'((?:[^\'\\]|\\.)*)', m.group(1))
    ]


def _get_int_from_tags(tags: list, category: str) -> Optional[int]:
    """Return the integer n from a tag like 'poolN' or 'rarityN', or None."""
    for tag in tags:
        m = re.match(rf"^{re.escape(category)}(\d+)$", tag)
        if m:
            return int(m.group(1))
    return None


def _parse_block(block: str) -> dict:
    tags = _get_str_array(block, "tags")
    return {
        "name":         _get_str(block, "name"),
        "title":        _get_str(block, "title"),
        "description":  _get_str(block, "description"),
        "flavourText":  _get_str(block, "flavourText"),
        "baseDamage":   _get_int(block, "baseDamage"),
        #"coverValue":   _get_int(block, "coverValue"),
        "cost":         _get_int(block, "cost"),
        "price":        _get_int(block, "price"),
        "dark":         _get_bool(block, "dark"),
        "tags":         tags,
        "traitEffects": _get_str_array(block, "traitEffects"),
        "pool":         _get_int_from_tags(tags, "pool"),
        "quantity":     _get_int_from_tags(tags, "rarity"),
    }


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def load_cards(path: Optional[Union[str, Path]] = None) -> list:
    """Parse cards.onj and return all card entries as dicts.

    Parameters
    ----------
    path : str or Path, optional
        Path to the cards.onj file. Defaults to cards.onj in the same
        directory as this script.

    Returns
    -------
    list[dict]
        One dict per card with keys: name, title, description, flavourText,
        baseDamage, cost, price, dark, tags, traitEffects.
    """
    src = Path(path) if path else _CARDS_ONJ
    try:
        text = src.read_text(encoding="utf-8")
    except OSError:
        # Loaded from a .apworld zip — the path is virtual, so use the zipimporter
        loader = getattr(__spec__, "loader", None)
        if loader and hasattr(loader, "get_data"):
            text = loader.get_data(str(src)).decode("utf-8")
        else:
            raise
    text = _strip_comments(text)
    cards = [_parse_block(b) for b in _extract_card_blocks(text)]
    return sorted(cards, key=lambda entry: (entry["name"] or "").lower())


def get_obtainable_cards(cards: Optional[list] = None) -> list:
    """Return cards that are neither tagged 'not used' nor 'unobtainable'.

    Parameters
    ----------
    cards : list[dict], optional
        Pre-loaded card list. If omitted, load_cards() is called.

    Returns
    -------
    list[dict]
    """
    resolved = cards if cards is not None else load_cards()
    return [
        entry for entry in resolved
        if "not used" not in entry["tags"] and "unobtainable" not in entry["tags"]
    ]


# ---------------------------------------------------------------------------
# Quick self-test when run directly
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    all_cards = load_cards()
    obtainable = get_obtainable_cards(all_cards)
    print(f"Total cards parsed : {len(all_cards)}")
    print(f"Obtainable cards   : {len(obtainable)}")
    print()
    for card in obtainable:
        print(f"  {card['title']:<32}  cost={card['cost']}  dmg={card['baseDamage']:<3}  quantity={card['quantity']}  pool={card['pool']}")
