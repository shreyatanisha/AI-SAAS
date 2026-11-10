from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text_into_chunks(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    return splitter.split_text(text)

if __name__ == "__main__":

    sample_text = "Our company develops AI chatbots. " * 100

    chunks = split_text_into_chunks(sample_text)

    print("Total chunks:", len(chunks))

    for index, chunk in enumerate(chunks):
        print(f"\nChunk {index + 1}:")
        print(chunk)
        
        
        
        
        
        

