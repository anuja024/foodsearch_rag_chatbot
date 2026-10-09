from src.vector_store import create_vector_store
from src.semantic_search import filtered_search_foods
import os
from dotenv import load_dotenv
from groq import Groq
load_dotenv()

def prepare_context(results):
    """Prepare context from search results for RAG."""
    context = ""

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    for i, (document, metadata) in enumerate(zip(documents, metadatas)):
        context += f"\nFood {i + 1}:\n"
        context += document
        context += f"\nCalories per serving: {metadata.get('calories', 'Not available')}\n"
        context += f"Cuisine: {metadata.get('cuisine_type', 'Not available')}\n"

    return context

def create_rag_prompt(query, context):
    """Create a prompt using the user's question and retrieved food information."""

    prompt = f"""
You are a food search and recommendation assistant.

You will receive food information retrieved from a database and a user's question.

Retrieved food information:
{context}

User question:
{query}

Instructions:
1. Answer using only the retrieved food information.
2. For calorie-limit questions, recommend only foods whose retrieved
   calorie metadata confirms that they satisfy the specified limit.
3. Never invent or estimate calories, ingredients, nutrients, health
   benefits, taste descriptions, or preparation details.
4. Report health benefits only when explicitly documented in the data.
5. Do not label a food healthy or unhealthy based on an individual benefit.
6. If health benefits are not documented, say that the data does not
   specify them.
7. If required information is missing, clearly state what is unavailable.
8. Do not assign food categories unless supported by the retrieved data.
9. Avoid repeating the same food name in the answer.
10. Keep the response concise, clear, and helpful.
11. Present results in a readable table when listing multiple foods.
12. Do not claim that the database contains all possible matching foods.
    Describe results as foods found in the retrieved information.
    
Answer:
"""
    return prompt

def generate_response(prompt):
    """Generate a response from the LLM."""
      # LLM integration will go here

    client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )
    chat_completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", 
             "content": "You are a helpful food recommendation assistant."},
            {"role": "user", 
             "content": prompt}
        ],
        max_tokens=500,
        temperature=0.3
    )

    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    collection = create_vector_store()
    query = "healthy sweet foods"
    results = filtered_search_foods(
        collection,
        query
    )

    context = prepare_context(results)
    prompt = create_rag_prompt(query, context)
    print(f"\nRAG Prompt:\n{prompt}")
    print(f"\nContext for RAG:\n{context}")

    response = generate_response(prompt)

    print("\n--- Assistant Response ---\n")
    print(response)