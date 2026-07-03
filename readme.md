# YouTube RAG Projects

This folder contains two hands-on **Retrieval-Augmented Generation (RAG)** projects that run
**100% locally** using [Ollama](https://ollama.com). No API keys, no cloud costs.

| Project | What it teaches | Data source | Stack |
| --- | --- | --- | --- |
| [`rag-level-1`](#project-1-rag-level-1) | RAG from scratch (no framework) | A single `.txt` file | `chromadb` + `ollama` |
| [`rag-langchain`](#project-2-rag-langchain) | Production-style, modular RAG | PDF files | `langchain` + `chromadb` + `ollama` |

Start with `rag-level-1` to understand the core idea, then move to `rag-langchain` to see
how the same pipeline is structured with a real framework.

---

## Prerequisites (do this once)

Both projects need the same local setup.

### 1. Install Python 3.10+

```bash
python3 --version
```

### 2. Install and start Ollama

Download from [ollama.com](https://ollama.com), then make sure the Ollama app/service is running.

```bash
ollama --version
```

### 3. Pull the required models

Both projects use one **embedding model** and one **chat model**:

```bash
# Embedding model (turns text into vectors)
ollama pull nomic-embed-text

# Chat / generation model (writes the final answer)
ollama pull llama3.1
```

> Tip: verify with `ollama list`. The first run of each model may be slow while it loads into memory.

---

## Project 1: `rag-level-1`

A minimal RAG pipeline written **without any framework** so you can see every step clearly:
chunk → embed → store → retrieve → generate.

### What it does

1. Reads text from `rag.txt`.
2. Splits it into ~600-character chunks with 100 characters of overlap.
3. Creates an embedding for each chunk with `nomic-embed-text`.
4. Stores the chunks + embeddings in a local **ChromaDB** database (`chroma_db/`).
5. Embeds a question, retrieves the 2 most similar chunks.
6. Sends the question + retrieved context to `llama3.1` and prints the answer.

### File overview

```
rag-level-1/
├── rag_level_1.py   # the entire pipeline in one script
├── rag.txt          # the knowledge source (edit this to change the data)
└── chroma_db/       # auto-created local vector database
```

### Run it — end to end

```bash
# 1. Go into the project
cd rag-level-1

# 2. (Recommended) create a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install chromadb ollama

# 4. Make sure Ollama is running and models are pulled (see Prerequisites)

# 5. Run the script
python rag_level_1.py
```

### What you'll see

The script prints the retrieved chunks, then the final generated answer to the
hard-coded question `"What is the RAG"`.

### Try it yourself

- Change the question: edit the `question = "..."` line in `rag_level_1.py`.
- Change the knowledge: replace the contents of `rag.txt` with your own text, then
  **delete the `chroma_db/` folder** and re-run so the new text is re-indexed.
- Tune retrieval: change `n_results` (how many chunks to fetch) or `chunk_size` /
  `chunk_overlap` (how the text is split).

---

## Project 2: `rag-langchain`

The same RAG idea, but built the **real-world way**: modular files, PDF ingestion,
LangChain loaders/splitters, and an interactive command-line menu.

### What it does

- **Loads PDFs** from `data/pdf_files/` using LangChain's `PyPDFLoader`.
- **Splits** documents with `RecursiveCharacterTextSplitter` (600 chars, 120 overlap).
- **Embeds** chunks with `nomic-embed-text` via `OllamaEmbeddings`.
- **Stores** everything in a persistent **ChromaDB** collection (`chroma_db/`).
- **Answers questions** by retrieving the top 3 chunks, building a prompt, and calling `llama3.1`.

### File overview

```
rag-langchain/
├── main.py            # interactive CLI: choose to index or query
├── loader.py          # loads all PDFs from the data/ folder
├── vectorstore.py     # chunking, embedding, storing & querying (ChromaDB)
├── rag_pipeline.py    # ties retrieval + prompt + LLM together
├── prompt.py          # builds the prompt sent to the model
├── requirement.txt    # Python dependencies
├── data/pdf_files/    # put your PDFs here (attention.pdf, Embeddings.pdf included)
└── chroma_db/         # auto-created local vector database
```

### Run it — end to end

```bash
# 1. Go into the project
cd rag-langchain

# 2. (Recommended) create a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirement.txt

# 4. Make sure Ollama is running and models are pulled (see Prerequisites)

# 5. Add your own PDFs to data/pdf_files/  (optional — samples are included)

# 6. Start the app
python main.py
```

### Using the interactive menu

When the app starts you'll see a menu:

```
1 For Indexing the documents   # read PDFs, chunk, embed, and store them
2 For Querying the documents   # ask a question against the stored documents
3 For Exiting the program
```

**First run:** choose `1` to index the PDFs. Then run again and choose `2` to ask questions.

Example session:

```
Enter your choice: 1
Indexing the documents...
Documents indexed successfully

Enter your choice: 2
Enter your query: What is attention in transformers?
... (generated answer) ...
```

### Try it yourself

- Add more PDFs to `data/pdf_files/` and re-index (choose `1`).
- Adjust retrieval quality: change `n_results` in `vectorstore.py` or the chunk sizes.
- Edit the assistant's behavior: change the template in `prompt.py`.
- Re-indexing note: to rebuild from scratch, delete the `chroma_db/` folder before indexing.

---

## How RAG works (quick recap)

Both projects follow the same core loop:

```
Documents ──chunk──► Text chunks ──embed──► Vectors ──store──► Vector DB (ChromaDB)
                                                                     │
Question ──embed──► Query vector ──similarity search──► Top matching chunks
                                                                     │
                     Question + retrieved chunks ──► LLM (llama3.1) ──► Answer
```

`rag-level-1` shows this with plain Python; `rag-langchain` shows the same flow with a
maintainable, framework-based structure.

---

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `Connection refused` / model errors | Make sure the Ollama app/service is running. |
| `model not found` | Run `ollama pull nomic-embed-text` and `ollama pull llama3.1`. |
| Answers ignore your new data | Delete the `chroma_db/` folder and re-index. |
| `ModuleNotFoundError` | Activate your virtual environment and re-run the `pip install` step. |
| Empty / irrelevant answers | Index the documents first (Project 2: choose `1`), and try smaller chunks. |
