import re
from src.vector_store import create_vector_store


def search_foods(collection, query, n_results=5):
    """Search for foods based on semantic similarity."""
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results


def filtered_search_foods(
    collection, query, max_calories=None, cuisine_type=None
):
    """Search foods using semantic similarity and optional filters."""

    filters = []

    if max_calories is not None:
        filters.append({"calories": {"$lte": max_calories}})

    if cuisine_type is not None:
        filters.append({"cuisine_type": cuisine_type})

    if len(filters) == 0:
        where = None
    elif len(filters) == 1:
        where = filters[0]
    else:
        where = {"$and": filters}

    # Retrieve extra results so duplicates can be removed.
    results = collection.query(
        query_texts=[query],
        n_results=15,
        where=where
    )

    # Keep only the first occurrence of each food name.
    seen_foods = set()
    unique_indices = []

    for i, metadata in enumerate(results["metadatas"][0]):
        food_name = metadata.get("food_name", "").strip().lower()

        if food_name and food_name not in seen_foods:
            seen_foods.add(food_name)
            unique_indices.append(i)

        if len(unique_indices) == 5:
            break

    # Preserve the original ChromaDB result structure.
    for key in ["ids", "documents", "metadatas", "distances"]:
        if key in results and results[key]:
            results[key][0] = [
                results[key][0][i] for i in unique_indices
            ]

    return results


def extract_max_calories(query):
    """Extract a maximum calorie value from a natural-language query."""

    patterns = [
        r"(?:under|below|less than|up to)\s*(\d+)\s*calories?",
        r"(\d+)\s*calories?\s*(?:or less|max|maximum)"
    ]

    for pattern in patterns:
        match = re.search(pattern, query.lower())

        if match:
            return int(match.group(1))

    return None


if __name__ == "__main__":
    collection = create_vector_store()

    results = filtered_search_foods(
        collection,
        "sweet foods",
        max_calories=300
    )

    print("\nUnique foods under 300 calories:\n")

    for metadata in results["metadatas"][0]:
        print(
            f"{metadata['food_name']} "
            f"-> {metadata['calories']} calories"
        )
