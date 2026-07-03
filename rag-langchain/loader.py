from langchain_community.document_loaders import PyPDFLoader, TextLoader
from pathlib import Path


def load_all_documents(path):

    path = Path(path)
    directory_path = path.glob("**/*.pdf")
    # print("directory_path", directory_path)

    documents = []


    for file in directory_path:
        print("file", file)
        loader = PyPDFLoader(file)
        data = loader.load()
        documents.extend(data)
        print("documents", documents)
    return documents

if __name__ == "__main__":
    documents = load_all_documents("data")
    print(len(documents))



