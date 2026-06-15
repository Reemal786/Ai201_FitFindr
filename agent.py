"""
agent.py

The FitFindr planning loop. Orchestrates the three tools in response to a
natural language user query, passing state between them via a session dict.

Complete tools.py and test each tool in isolation before implementing this file.
"""

import re

from tools import search_listings, suggest_outfit, create_fit_card


def _new_session(query: str, wardrobe: dict) -> dict:
    return {
        "query": query,
        "parsed": {},
        "search_results": [],
        "selected_item": None,
        "wardrobe": wardrobe,
        "outfit_suggestion": None,
        "fit_card": None,
        "error": None,
    }


def run_agent(query: str, wardrobe: dict) -> dict:
    session = _new_session(query, wardrobe)

    price_match = re.search(
        r"(?:under|below|less than|\$)\s*\$?(\d+(?:\.\d+)?)",
        query.lower()
    )
    max_price = float(price_match.group(1)) if price_match else None

    size_match = re.search(r"size\s+([a-zA-Z0-9/]+)", query.lower())
    size = size_match.group(1).upper() if size_match else None

    description = query.lower()
    description = re.sub(r"(?:under|below|less than|\$)\s*\$?\d+(?:\.\d+)?", "", description)
    description = re.sub(r"size\s+[a-zA-Z0-9/]+", "", description)
    description = description.replace("looking for", "")
    description = description.replace("i'm", "")
    description = description.replace("im", "")
    description = description.strip(" ,.")

    session["parsed"] = {
        "description": description,
        "size": size,
        "max_price": max_price,
    }

    results = search_listings(description, size=size, max_price=max_price)
    session["search_results"] = results

    if not results:
        session["error"] = (
            "No matching listings were found. Try broadening the description, "
            "increasing the budget, or removing the size filter."
        )
        return session

    selected_item = results[0]
    session["selected_item"] = selected_item

    outfit = suggest_outfit(selected_item, wardrobe)
    session["outfit_suggestion"] = outfit

    if not outfit or not outfit.strip():
        session["error"] = "An outfit suggestion could not be created for this item."
        return session

    fit_card = create_fit_card(outfit, selected_item)
    session["fit_card"] = fit_card

    return session


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== Happy path: graphic tee ===\n")
    session = run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    )

    if session["error"]:
        print(f"Error: {session['error']}")
    else:
        print(f"Found: {session['selected_item']['title']}")
        print(f"\nOutfit: {session['outfit_suggestion']}")
        print(f"\nFit card: {session['fit_card']}")

    print("\n\n=== No-results path ===\n")
    session2 = run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    )
    print(f"Error message: {session2['error']}")