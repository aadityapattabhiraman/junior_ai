import Levenshtein
from sqlalchemy import create_engine, and_
from sqlalchemy.engine import URL
import pandas as pd
import torch
from transformers import LlamaTokenizer, LlamaForCausalLM, pipeline
from langchain_community.llms import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
import warnings
warnings.filterwarnings("ignore")
import logging
logging.disable(logging.CRITICAL)




def jaccard_similarity(str1, str2):
    set1 = set(str1)
    set2 = set(str2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union

def find_closest_string(input_string, string_list):
    closest_string = None
    max_similarity = 0
    for string in string_list:
        similarity = jaccard_similarity(input_string, string)
        if similarity > max_similarity:
            max_similarity = similarity
            closest_string = string
    return closest_string

def get_llm_response(tble,question,cols, prompt, local_llm):
    llm_chain = LLMChain(prompt=prompt, 
                         llm=local_llm
                         )
    response= llm_chain.run({"Table" : tble,"question" :question, "Columns" : cols})
    return (response)

def trial(text):
    url = URL.create(
        drivername="postgresql",
        username="hitman",
        host="localhost",
        database="trial")

    engine = create_engine(url)

    sql = "select * from review"
    tble = "review"
    cols = pd.read_sql(sql, engine)
    cols = cols.drop(["index"], axis=1)
    cols = list(cols.columns)

    base_model = LlamaForCausalLM.from_pretrained(
        "chavinlo/alpaca-native",
        load_in_4bit=True,
        device_map='auto',
    )

    tokenizer = LlamaTokenizer.from_pretrained("chavinlo/alpaca-native")

    pipe = pipeline(
        "text-generation",
        model=base_model,
        tokenizer=tokenizer,
        max_length=500,
        temperature=0.3,
        top_p=0.95,
        repetition_penalty=1.2
    )

    local_llm = HuggingFacePipeline(pipeline=pipe)


    question = text
    print(question)
    template = """
    Write a SQL Query given the table name {Table} and columns as a list {Columns} for the given question : 
    {question}.
    """

    prompt = PromptTemplate(template=template, input_variables=["Table","question","Columns"])

    sql = get_llm_response(tble,question,cols, prompt, local_llm)
    sql = sql.split("\n")[-1]
    sql = sql.split(" ")

    count = -1
    start = 0
    for k in sql:
        count += 1
        if k in ["SELECT", "FROM", "WHERE"]:
            if k == "WHERE":
                start = 1
            continue
        if start==0:
            continue
        for z in cols:
            if k in z or z in k:
                sql[count] = z
                break


    ind = sql.index("FROM") + 1
    sql[ind] = tble
    sql = " ".join(sql)
    print(sql)
    fin = pd.read_sql(sql, engine).values.tolist()
    text = ""

    for i in fin:
        for j in i:
            if type(j) == int:
                return j
            else:
                text += str(j)
                text += ", "

    if len(text) > 300:
        text = text[:300]
        print(text)

    return text

# print(trial("Query that gives the count of companies where the rating are more than 4."))