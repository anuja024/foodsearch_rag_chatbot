# 🍽️ Food Search & RAG Chatbot

An AI-powered food search application that uses semantic search and Retrieval-Augmented Generation (RAG) to answer questions about food, ingredients, cuisines, documented health benefits, and calorie limits.

## ✨ Features

- **Semantic Search:** Retrieves relevant food information using Sentence Transformers embeddings.
- **RAG Pipeline:** Uses retrieved context to generate responses with the Groq API.
- **Calorie Filtering:** Filters foods by maximum calorie limits using ChromaDB metadata.
- **Ingredient & Cuisine Search:** Finds foods based on queries about ingredients and cuisines.
- **Interactive Web Interface:** Provides a conversational interface built with Gradio.
- **Context-Grounded Responses:** Instructs the language model to use retrieved information and avoid unsupported claims.

## 🛠️ Tech Stack

- Python
- ChromaDB
- Sentence Transformers
- Groq API
- Gradio

## ⚙️ How It Works

1. Food records are loaded from a JSON dataset.
2. Sentence Transformers generates embeddings for semantic retrieval.
3. ChromaDB stores the food information and metadata.
4. User queries retrieve relevant records, optionally filtered by calorie limits.
5. The retrieved information is assembled into context.
6. The Groq API generates a response based on that context.
7. Gradio displays the response through the web interface.

## 🚀 Setup and Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd food_rag_chatbot
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Replace the placeholder with your own Groq API key. Never commit your `.env` file.

### 5. Run the application

```bash
python app.py
```

Open the local URL displayed in the terminal.

## 📁 Project Structure

```text
food_rag_chatbot/
├── data/
│   └── FoodDataSet.json
├── src/
│   ├── data_loader.py
│   ├── vector_store.py
│   ├── semantic_search.py
│   ├── rag.py
│   └── chatbot.py
├── app.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

The ChromaDB persistence directory is generated locally when the application initializes the vector store.

## ⚠️ Limitations

- Search quality depends on the coverage and quality of the current dataset.
- Nutrition and health-related information may be incomplete or inaccurate.
- Generated answers should not be treated as medical or dietary advice.
- A valid Groq API key and an internet connection are required for LLM responses.

## 🔮 Future Improvements

- Expand the dataset with reliable food-composition sources.
- Improve duplicate detection and retrieval relevance.
- Add more structured nutritional attributes.
- Add automated tests and improve error handling.

## 👩‍💻 Author

Anuja Jadhav
