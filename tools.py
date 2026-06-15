"""
tools.py

The three required FitFindr tools. Each tool is a standalone function that
can be called and tested independently before being wired into the agent loop.

Complete and test each tool before moving to agent.py.

Tools:
    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)              → str
    create_fit_card(outfit, new_item)               → str
"""

import os

from dotenv import load_dotenv
from groq import Groq

from utils.data_loader import load_listings

load_dotenv()


# ── Groq client ───────────────────────────────────────────────────────────────

def _get_groq_client():
    """Initialize and return a Groq client using GROQ_API_KEY from .env."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not set. Add it to a .env file in the project root."
        )
    return Groq(api_key=api_key)


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the mock listings dataset for items matching the description,
    optional size, and optional price ceiling.

    Args:
        description: Keywords describing what the user is looking for
                     (e.g., "vintage graphic tee").
        size:        Size string to filter by, or None to skip size filtering.
                     Matching is case-insensitive (e.g., "M" matches "S/M").
        max_price:   Maximum price (inclusive), or None to skip price filtering.

    Returns:
        A list of matching listing dicts, sorted by relevance (best match first).
        Returns an empty list if nothing matches — does NOT raise an exception.

    Each listing dict has the following fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand, platform

    TODO:
        1. Load all listings with load_listings().
        2. Filter by max_price and size (if provided).
        3. Score each remaining listing by keyword overlap with `description`.
        4. Drop any listings with a score of 0 (no relevant matches).
        5. Sort by score, highest first, and return the listing dicts.

    Before writing code, fill in the Tool 1 section of planning.md.
    """
    listings = load_listings()

    if not description:
        return []

    search_words = set(description.lower().split())
    matches = []

    for item in listings:
        if max_price is not None and item.get("price", 0) > max_price:
            continue

        if size is not None:
            item_size = str(item.get("size", "")).lower()
            if size.lower() not in item_size:
                continue

        text_parts = [
            str(item.get("title") or ""),
            str(item.get("description") or ""),
            str(item.get("category") or ""),
            str(item.get("brand") or ""),
            str(item.get("condition") or ""),
            " ".join(item.get("style_tags") or []),
            " ".join(item.get("colors") or []),
        ]

        searchable_text = " ".join(text_parts).lower()

        score = 0
        for word in search_words:
            if word in searchable_text:
                score += 1

        if score > 0:
            matches.append((score, item))

    matches.sort(key=lambda result: result[0], reverse=True)

    return [item for score, item in matches]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest 1–2 complete outfits.

    Args:
        new_item: A listing dict (the item the user is considering buying).
        wardrobe: A wardrobe dict with an 'items' key containing a list of
                  wardrobe item dicts. May be empty — handle this gracefully.

    Returns:
        A non-empty string with outfit suggestions.
        If the wardrobe is empty, offer general styling advice for the item
        rather than raising an exception or returning an empty string.

    TODO:
        1. Check whether wardrobe['items'] is empty.
        2. If empty: call the LLM with a prompt for general styling ideas
           (what kinds of items pair well, what vibe it suits, etc.).
        3. If not empty: format the wardrobe items into a prompt and ask
           the LLM to suggest specific outfit combinations using the new item
           and named pieces from the wardrobe.
        4. Return the LLM's response as a string.

    Before writing code, fill in the Tool 2 section of planning.md.
    """
    client = _get_groq_client()

    wardrobe_items = wardrobe.get("items", []) if wardrobe else []

    item_info = f"""
Title: {new_item.get("title", "Unknown item")}
Description: {new_item.get("description", "")}
Category: {new_item.get("category", "")}
Colors: {new_item.get("colors", [])}
Style tags: {new_item.get("style_tags", [])}
Price: ${new_item.get("price", "")}
Platform: {new_item.get("platform", "")}
"""

    if not wardrobe_items:
        prompt = f"""
You are FitFindr, a helpful secondhand fashion styling assistant.

The user found this thrifted item:

{item_info}

The user's wardrobe is empty or unavailable.

Suggest 1 complete outfit using general styling advice. Be specific, practical, and concise.
Do not say you cannot help.
"""
    else:
        wardrobe_text = "\n".join(
            [
                f"- {item.get('name', item.get('title', 'Item'))}: "
                f"{item.get('category', '')}, colors: {item.get('colors', [])}, "
                f"style: {item.get('style_tags', [])}"
                for item in wardrobe_items
            ]
        )

        prompt = f"""
You are FitFindr, a helpful secondhand fashion styling assistant.

The user found this thrifted item:

{item_info}

Here is the user's wardrobe:

{wardrobe_text}

Suggest 1-2 complete outfits using the thrifted item and specific pieces from the wardrobe.
Keep the response concise, useful, and natural.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a concise fashion styling assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Generate a short, shareable outfit caption for the thrifted find.

    Args:
        outfit:   The outfit suggestion string from suggest_outfit().
        new_item: The listing dict for the thrifted item.

    Returns:
        A 2–4 sentence string usable as an Instagram/TikTok caption.
        If outfit is empty or missing, return a descriptive error message
        string — do NOT raise an exception.

    The caption should:
    - Feel casual and authentic (like a real OOTD post, not a product description)
    - Mention the item name, price, and platform naturally (once each)
    - Capture the outfit vibe in specific terms
    - Sound different each time for different inputs (use higher LLM temperature)

    TODO:
        1. Guard against an empty or whitespace-only outfit string.
        2. Build a prompt that gives the LLM the item details and the outfit,
           and asks for a caption matching the style guidelines above.
        3. Call the LLM and return the response.

    Before writing code, fill in the Tool 3 section of planning.md.
    """
    if not outfit or not outfit.strip():
        return "Cannot create a fit card because the outfit suggestion is missing."

    client = _get_groq_client()

    prompt = f"""
Create a short, shareable outfit caption for a thrifted fashion find.

Item details:
Title: {new_item.get("title", "Unknown item")}
Price: ${new_item.get("price", "")}
Platform: {new_item.get("platform", "")}
Condition: {new_item.get("condition", "")}
Brand: {new_item.get("brand", "")}

Outfit suggestion:
{outfit}

Requirements:
- 2-4 sentences
- Casual and authentic, like a real OOTD post
- Mention the item name, price, and platform naturally once
- Capture the outfit vibe
- Do not sound like an advertisement
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You write casual social media outfit captions."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.9,
    )

    return response.choices[0].message.content.strip()