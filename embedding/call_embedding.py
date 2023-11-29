import os
from embedding.zhipuai_embedding import ZhipuAIEmbeddings
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from llm.call_llm import parse_llm_api_key

def get_embedding(embedding: str, embedding_key: str=None, env_file: str=None):
    if embedding_key == None:
        embedding_key = parse_llm_api_key(embedding)
    if embedding == "openai":
        os.environ['http_proxy'] = 'http://127.0.0.1:10809'
        os.environ['https_proxy'] = 'http://127.0.0.1:10809'
        return OpenAIEmbeddings(openai_api_key=embedding_key)
    elif embedding == "zhipuai":
        return ZhipuAIEmbeddings(zhipuai_api_key=embedding_key)
    elif embedding == 'm3e':
        os.environ['http_proxy'] = 'http://127.0.0.1:10809'
        os.environ['https_proxy'] = 'http://127.0.0.1:10809'
        return HuggingFaceEmbeddings(model_name="moka-ai/m3e-base")
    else:
        raise ValueError(f"embedding {embedding} not support ")
