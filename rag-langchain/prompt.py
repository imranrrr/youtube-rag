
def get_prompt(context, query):
    prompt = f"""
    You are a helpful assistant that can answer questions about the documents.
    You are given a question and a context.
    You need to answer the question based on the context.
    Context: 
    {context}
    Question: 
    {query}
    Answer:
    """


    return prompt;


if __name__ == "__main__":
    context = "The capital of France is Paris."
    query = "What is the capital of France?"
    prompt = get_prompt(context, query)
    print(prompt)