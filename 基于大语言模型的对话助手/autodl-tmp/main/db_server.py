from fastapi import FastAPI
import os
from langchain_community.vectorstores import FAISS
from create_database import get_embeddings
from configs import rag_configs

# 读取所有的db
db_path = rag_configs["database"]["db_vector_path"]
index_names = set([os.path.splitext(i)[0] for i in os.listdir(db_path)])
embedding = get_embeddings(rag_configs["embedding"])

index_map = {
    name: FAISS.load_local(
        db_path,
        index_name=name,
        embeddings=embedding,
        allow_dangerous_deserialization=True,
    )
    for name in index_names
}


app = FastAPI()

#FastAPI 特点
#高性能： 基于Starlette和Pydantic，利用异步（asynchronous）编程，提供出色的性能。
#自动文档生成： 自动生成交互式API文档，支持Swagger UI和ReDoc，让API的理解和测试更加直观。
#类型注解支持： 利用Python的类型提示，提供更严格的输入验证和更好的代码提示。
#异步支持： 支持异步请求处理，使得处理IO密集型任务更加高效。
#FastAPI 建立在 Starlette 和 Pydantic 之上，利用类型提示进行数据处理，并自动生成API文档。

# 检索相关知识
@app.get("/db/v1/retriever")
async def get_relantic_documents(query: str, index_name: str, k: int = 1):
    if index_name not in index_names:
        return {"Error": f"not find {index_name}."}
    if k < 1:
        return {"Error": f"k={k}, must be bigger than 1"}
    if not query:
        return {"Error": f"query must be not empty."}
    vectore = index_map[index_name]
    docs = vectore.similarity_search_with_relevance_scores(query, k=k)
    docs = [
        {"doc": d[0].page_content, "metadata": d[0].metadata, "score": d[1]}
        for d in docs
    ]

    return docs


# 获取所有的知识库
@app.get("/db/v1/index_name/")
async def get_index_names():
    return {"index-names": index_names}


# 查询数据库
# import requests
# response = requests.get(
#     "http://localhost:8000/db/v1/retriever?query=rag&index_name=db1&k=3"
# )
# print(response.json())

# 产看所有的数据库
# import requests
# response = requests.get("http://localhost:8000/db/v1/index_name")
# print(response.json())