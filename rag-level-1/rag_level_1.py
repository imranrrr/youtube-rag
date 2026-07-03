#Chromabd => as a vector database => for storing and querying embeddings
#LLM => OLLAM => LOCAL
#ollama => embedding ollama 


from calendar import c
import chromadb;
import ollama;
from pathlib import Path;

client = chromadb.PersistentClient(path="chroma_db");

collection = client.get_or_create_collection(name="youtube-rag");


#chunks of the data
data = Path("rag.txt").read_text(encoding="utf-8");

chunks = []
start = 0 
chunk_size = 600;
chunk_overlap = 100;

while start < len(data):
    end  = start + chunk_size;
    chunk = data[start:end]

    if chunk.strip():
        chunks.append(chunk)

    start = end - chunk_overlap;

for index, chunk in enumerate(chunks):
    embedding_response = ollama.embeddings(model="nomic-embed-text", prompt=chunk)

    embedding = embedding_response["embedding"]
    # print(embedding)
    # print(f"embedding for chunk {index} has been created {embedding}")

    collection.add(
        documents=[chunk],
        embeddings=embedding, 
        ids=[str(index)]
    )



question = "What is the RAG"


question_embedding = ollama.embeddings(model="nomic-embed-text", prompt=question)
question_embedding = question_embedding["embedding"]

results = collection.query(
   query_embeddings = question_embedding,
    n_results=2,
)

documents = results["documents"][0]

print(documents)

final_response = ollama.chat(model="llama3.1:latest", messages=[
    {
        "role": "user",
        "content": f"Answer the following question: {question} \n\n {documents}"
    }
])
print("-------------")
print(final_response["message"]["content"])