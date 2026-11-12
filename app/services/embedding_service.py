from langchain_community.embeddings import FastEmbedEmbeddings

_embeddings = None


def get_embeddings():
    global _embeddings
    if _embeddings is None:
        _embeddings = FastEmbedEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            batch_size=16,
            threads=1
        )
    return _embeddings


def generate_embeddings(text: str):
    return get_embeddings().embed_query(text)


def generate_document_embeddings(texts: list[str]):
    return get_embeddings().embed_documents(texts)


def embed_text_chunks(chunks: list[str]):
    return get_embeddings().embed_documents(chunks)

if __name__ == "__main__":
    question = "What services does our company provide?"

    vector = generate_embeddings(question)

    print("Embedding dimensions:", len(vector))
    print("First 5 values:", vector[:5])
