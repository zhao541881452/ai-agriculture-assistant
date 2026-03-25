from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
import os

# 👉 读取PDF
def load_documents():
    docs = []
    folder = "data"

    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(folder, file))
            docs.extend(loader.load())

    return docs

# 👉 加载文档
documents = load_documents()

# 👉 切分
splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = splitter.split_documents(documents)

# 👉 向量模型
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 👉 建库
db = FAISS.from_documents(texts, embeddings)

# 👉 查询
def search_knowledge(query):
    results = db.similarity_search(query, k=3)
    return "\n".join([r.page_content for r in results])
