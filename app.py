import gradio as gr

from src.vector_store import create_vector_store
from src.semantic_search import filtered_search_foods, extract_max_calories
from src.rag import prepare_context, create_rag_prompt, generate_response


# Initialize the vector database once when the app starts
collection = create_vector_store()


def respond(message, history):
    """Generate a response to the user's food query."""

    if not message or not message.strip():
        return "Please enter a food-related question."

    max_calories = extract_max_calories(message)

    results = filtered_search_foods(
        collection,
        message,
        max_calories=max_calories
    )

    if not results["documents"][0]:
        return "No matching foods were found. Try a different query or calorie limit."

    context = prepare_context(results)
    prompt = create_rag_prompt(message, context)

    return generate_response(prompt)


theme = gr.themes.Soft(
    primary_hue="green",
    secondary_hue="lime",
    neutral_hue="slate"
)

css = """
.gradio-container {
    max-width: 1000px !important;
    margin: auto !important;
}
#app-title {
    text-align: center;
}
#app-subtitle {
    text-align: center;
    max-width: 700px;
    margin: auto;
}
"""

with gr.Blocks(theme=theme, css=css, title="Food Search & RAG Chatbot") as demo:

    gr.Markdown(
        """
        # 🍽️ Food Search & RAG Chatbot
        """,
        elem_id="app-title"
    )

    gr.Markdown(
        """
        Discover foods through semantic search and AI-powered answers.
        Explore cuisines, ingredients, documented health benefits, and calorie limits.
        """,
        elem_id="app-subtitle"
    )

    gr.Markdown("### 💬 Ask your food question")

    gr.ChatInterface(
        fn=respond,
        examples=[
            "Italian food",
            "Foods with coconut",
            "Healthy sweet foods under 300 calories",
            "Indian food under 400 calories"
        ],
        textbox=gr.Textbox(
            placeholder="Try asking: Indian food under 400 calories",
            container=False
        ),
        show_progress="minimal"
    )

    gr.Markdown(
        """
        ---
        **How it works:** Sentence Transformers + ChromaDB retrieve relevant
        food information, and Groq generates an answer grounded in that context.

        <small>Food information is based on the project's dataset and may not
        represent complete nutritional advice.</small>
        """
    )


if __name__ == "__main__":
    demo.launch()