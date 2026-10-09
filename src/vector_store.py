import chromadb
from chromadb.utils import embedding_functions
from src.data_loader import load_food_data

def create_vector_store():
    """Create a ChromaDB collection using Sentence Transformers."""
    client = chromadb.PersistentClient(path = "chroma_db")
    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
    
    collection = client.get_or_create_collection(
        name="food_collection",
        configuration={
            "hnsw":{"space": "cosine"}
        },
        embedding_function=embedding_function
        )
    return collection

def add_food_data_to_collection(collection, food_data):
    """Add food data to the ChromaDB collection."""

    documents = []
    metadatas = []
    ids = []

    for food in food_data:
        food_id = str(food["food_id"])

        document = (
            f"Food Name: {food['food_name']}\n"
            f"Food Description: {food['food_description']}\n"
            f"Ingredients: {food['food_ingredients']}\n"
            f"Cuisines: {food['cuisine_type']}\n"
            f"Cooking Method: {food['cooking_method']}\n"
            f"Health Benefits: {food['food_health_benefits']}\n"
            f"taste: {food['food_features']['taste']}\n"
        )
        documents.append(document)

        metadatas.append({
            "food_id": food_id,
            "food_name": food["food_name"],
            "cuisines": food["cuisine_type"],
            "calories": food["food_calories_per_serving"]
        })
        ids.append(f"{food_id}_{len(ids)}")  # Ensure unique IDs by appending the index

    collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
    )

    return collection
       

if __name__ == "__main__":
    food_data = load_food_data("data/FoodDataSet.json")
    collection = create_vector_store()
    add_food_data_to_collection(collection, food_data)
    print(f"Added {len(food_data)} food records to the ChromaDB collection.")
