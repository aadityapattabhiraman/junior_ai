from langchain_community.document_loaders import TextLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer
import transformers
import torch
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
import warnings
import logging


def rag(prompt: str) -> str:
    model="TheBloke/Llama-2-7B-Chat-GPTQ"
    tokenizer=AutoTokenizer.from_pretrained(model)

    pipeline=transformers.pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        device_map="auto",
        max_length=1000,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id
    )

    llm=HuggingFacePipeline(pipeline=pipeline, model_kwargs={'temperature':0})

    loader = TextLoader("data.txt")
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    all_splits = text_splitter.split_documents(data)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = Chroma.from_documents(documents=all_splits, embedding=embeddings)

    q = prompt
    retriever = db.as_retriever(
        search_type="mmr"
    )
    context = retriever.invoke(prompt)

    template = """
        Based on the given context {context} try to answer the given question if you don't know then say don't know.: 
        {question}.
        """

    prompt = PromptTemplate(template=template, input_variables=["context", "question"])

    llm_chain = LLMChain(prompt=prompt, llm=llm)

    response = llm_chain.run({"context" : context, "question" :q})
    del llm
    answer = response.split("\n")
    answer = "\n".join(answer[-2:])

    return answer


if __name__ == "__main__":
    logging.disable(logging.CRITICAL)
    warnings.filterwarnings("ignore")
    answer = rag("What was the actual sales achieved by chromoatography division in the month of march?")
    answer = answer.split("\n")
    answer = "\n".join(answer[-2:])
    print(answer)