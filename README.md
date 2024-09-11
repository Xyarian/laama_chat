# Laama Chat - AI Chat Application

Laama Chat is a [Streamlit](https://streamlit.io/) based application that provides an interactive chat interface using the [Llama 3.1 8B](https://llama.meta.com/) and [Gemma 2 9B](https://ai.google.dev/gemma) **locally**. Users can engage in conversations, upload documents for context, and save/load chat sessions with their preferred model.

## Features

- 🤖 Chat interface powered by multiple AI models (Llama 3.1 and Gemma 2)
- 🔄 Ability to switch between different models for each chat session
- 📄 Document upload support for context-aware conversations
- 💾 Save and load chat sessions with SQLite, including model selection
- 🎨 Custom-styled UI built with Streamlit
- 🔧 Extensibility to easily add support for other Ollama models

## Installation

### Prerequisites

- Python
- Ollama

[![Python Version](https://img.shields.io/badge/python-3.12.5-blue)](https://www.python.org/downloads/)
[![Ollama Version](https://img.shields.io/badge/ollama-0.3.5-green)](https://ollama.ai)
[![Streamlit Version](https://img.shields.io/badge/streamlit-1.37.1-red)](https://streamlit.io/)

### Setup

1. Install Ollama and the Llama 3.1 8B model:
Follow the instructions at [Ollama's official website](https://ollama.ai/) or https://github.com/ollama/ollama to install Ollama and download the models. E.g. once Ollama is installed:

```
ollama pull llama3.1
```

and / or

```
ollama pull gemma2
```

2. Clone the repository:

```
git clone https://github.com/Xyarian/laama_chat.git
cd laama_chat
```

3. Create a virtual environment:

- Windows:

  ```
  python -m venv .venv
  .venv\Scripts\activate
  ```

- Linux/macOS:

  ```
  python3 -m venv venv
  source venv/bin/activate
  ```

4. Install dependencies:

Basic use case:
```
pip install -r requirements.txt
```

For RAG (Retrieval-Augmented Generation) functionality with laama_chat_rag.py:
```
pip install -r requirements_rag.txt
```

## Usage

1. Run the Streamlit app:

```
streamlit run laama_chat.py
```

2. Open your web browser and navigate to the URL displayed in the terminal (`http://localhost:8501`).

3. Start chatting with Laama, upload documents, or use the sidebar to manage chat sessions.

## Extending Model Support

To add support for additional Ollama models:

Update the `MODEL_MAPPING` dictionary in `laama_chat.py` to include the new model.
Ensure the model is available through [Ollama](https://ollama.com/library).

## Project Structure

```
laama_chat /
├── .streamlit/
│   └── config.toml
│   └── secrets.toml (for local RAG use case)
├── files/
│   └── bg_image.png
├── htmlTemplates.py
├── laama_chat_rag.py
├── laama_chat.py
├── chats_db.py
├── requirements_rag.txt (for laama_chat_rag.py use case)
└── requirements.txt


```

## Offline Mode

The RAG functionality (laama_chat_rag.py) supports full offline mode:

- The BAAI/bge-base-en-v1.5 model is stored locally. You can download it from Hugging Face and store it in the directory of your choice.
- Environment variables are set to enforce offline mode for Hugging Face libraries.
- The `.streamlit/secrets.toml` file is used to specify the local path to the model.

Example `secrets.toml` content:

```
[local_model]
path = "/path/to/your/local/model"
```

TODO: Additional notes to be added later for RAG implementation.

### Dependencies

See requirements.txt for a list of Python dependencies.

### Acknowledgements

- [Llama 3.1](https://llama.meta.com/)
- [Gemma 2](https://ai.google.dev/gemma)
- [Ollama](https://ollama.ai/)
- [Streamlit](https://streamlit.io/)

### Screenshots

![Screenshot 1](https://github.com/user-attachments/assets/299a2869-dd4b-4ac1-b8da-99aa085266b8)

![Screenshot 2](https://github.com/user-attachments/assets/bdf6b88a-5046-4f92-a176-58e5fa75924c)

### License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
