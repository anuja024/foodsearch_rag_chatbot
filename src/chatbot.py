from vector_store import create_vector_store
from semantic_search import extract_max_calories, filtered_search_foods
from rag import prepare_context, create_rag_prompt, generate_response


def chat():
    """Run the interactive food recommendation chatbot."""

    collection = create_vector_store()

    print("\n🍽️ Food RAG Chatbot")
    print("Ask me about foods, ingredients, cuisines, or health benefits.")
    print("Type 'quit' to exit.\n")

    while True:

        query = input("You: ").strip()

        if query.lower() == "help":
            print("""
You can ask me about:
- foods from a specific cuisine
- ingredients
- taste
- health benefits
- calorie limits

Examples:
- Italian food
- foods with coconut
- healthy sweet foods
- Indian food under 300 calories
"""         )
            continue

        if query.lower() == "quit":
            print("\nGoodbye! 👋")
            break

        if not query:
            continue

        
        max_calories = extract_max_calories(query)
        # 1. Retrieve relevant foods
        results = filtered_search_foods(
            collection,
            query,
            max_calories=max_calories
        )

        # 2. Build context
        context = prepare_context(results)

        # 3. Build RAG prompt
        prompt = create_rag_prompt(query, context)

        # 4. Generate answer
        response = generate_response(prompt)

        print(f"\nBot: {response}\n")


if __name__ == "__main__":
    chat()