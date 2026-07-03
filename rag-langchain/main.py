from vectorstore import Vectorstore
from loader import load_all_documents
from rag_pipeline import RAGPipeline

if __name__ == "__main__":  
    while True:
        print("Starting RAG pipeline...")   
        print("1 For Indexing the documents")
        print("2 For Querying the documents")
        print("3 For Exiting the program")
        vectorstore = Vectorstore()
        choice = input("Enter your choice: ")
        if choice == "1":
            print("Indexing the documents...")  
            documents = load_all_documents("data")
            vectorstore.add_collection(documents)
            print("Documents indexed successfully")
        elif choice == "2":
            print("Querying the documents...")
            query = input("Enter your query: ")
            rag_pipeline = RAGPipeline()
            results = rag_pipeline.get_relevant_documents(query)
            print(results)
        elif choice == "3":
            print("Exiting the program...")
            exit()
        else:
            print("Invalid choice")
            exit()