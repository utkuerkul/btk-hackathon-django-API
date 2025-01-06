from PyPDF2 import PdfReader
pdfreader = PdfReader(<PDF Document which you want query>)

from typing_extensions import Concatenate
# read text from pdf
raw_text = ''
for i, page in enumerate(pdfreader.pages):
    content = page.extract_text()
    if content:
        raw_text += content

max_tokens = 1000
tokenizer = Tokenizer.from_pretrained("bert-base-uncased")
splitter = TextSplitter.from_huggingface_tokenizer(tokenizer, max_tokens)

chunks = splitter.chunks(raw_text)
chunks

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Typesense

embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", task_type="retrieval_document")

docsearch = Typesense.from_texts(
    res,
    chunks,
    typesense_client_params={
        "host": "localhost",  # Use xxx.a1.typesense.net for Typesense Cloud
        "port": "8108",  # Use 443 for Typesense Cloud
        "protocol": "http",  # Use https for Typesense Cloud
        "typesense_api_key": "xyz",
        "typesense_collection_name": "gemini-with-typesense",
    },
)

from langchain.chains.question_answering import load_qa_chain

llm = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True)
chain = load_qa_chain(llm, chain_type="stuff")

question = "What is Scaled Dot-Product Attention?"

retriever = docsearch.as_retriever()
docs = retriever.invoke(question)
chain.run(input_documents=docs, question=question)

