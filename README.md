# Laama Chat - (Llama 3.1)

Laama Chat is a [Streamlit](https://streamlit.io/) -based application that provides an interactive chat interface using the [Llama 3.1 8B](https://llama.meta.com/) model. Users can engage in conversations, upload documents for context, and save/load chat sessions.

## Features

- 🤖 Advanced chat interface powered by Llama 3.1 8B model
- 📄 Document upload support for context-aware conversations
- 💾 Save and load chat sessions with SQLite
- 🎨 Custom-styled UI built with Streamlit


## Installation

### Prerequisites

- Python
- Ollama

[![Python Version](https://img.shields.io/badge/python-3.12.5-blue)](https://www.python.org/downloads/)
[![Ollama Version](https://img.shields.io/badge/ollama-0.3.5-green)](https://ollama.ai)
[![Streamlit Version](https://img.shields.io/badge/streamlit-1.37.1-red)](https://streamlit.io/)

### Setup

1. Install Ollama and the Llama 3.1 8B model:
Follow the instructions at [Ollama's official website](https://ollama.ai/) or https://github.com/ollama/ollama to install Ollama and download the Llama 3.1 8B model. E.g. once Ollama is installed:

```
ollama pull llama3.1
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

```
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:

```
streamlit run laama_chat.py
```

2. Open your web browser and navigate to the URL displayed in the terminal (`http://localhost:8501`).

3. Start chatting with Laama, upload documents, or use the sidebar to manage chat sessions.

## Project Structure

```
laama_chat /
├── .streamlit/
│   └── config.toml
├── css/
│   └── styles.css
├── files/
│   └── bg_image.png
├── laama_chat.py
├── chats_db.py
└── requirements.txt

```

### Dependencies

See requirements.txt for a list of Python dependencies.

### Acknowledgements

- [Llama 3.1](https://llama.meta.com/)
- [Ollama](https://ollama.ai/)
- [Streamlit](https://streamlit.io/)

### Screenshots

![Screenshot 1](https://github.com/user-attachments/assets/299a2869-dd4b-4ac1-b8da-99aa085266b8)

![Screenshot 2](https://github.com/user-attachments/assets/2565fa92-c0aa-4108-beab-5a80c72181a9)

### License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
