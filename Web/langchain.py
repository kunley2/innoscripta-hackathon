from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, LLMRequestsChain
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.document_loaders import WebBaseLoader,UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQAWithSourcesChain,RetrievalQA
from dotenv import load_dotenv

load_dotenv()
import os

openai_api_key = os.getenv("OPENAI_API_KEY")
serp_key = os.getenv("SERP_API_KEY")


def output_value(result):
    value = list(map(lambda x:x['result'],result))
    data = {
        'overview':value[0],
        'products':value[1],
        'keywords':value[2],
        'image':value[3],
        'address':value[4]
    }
    return data


def lang_chain(company,country,api_key=serp_key):
  """ This function takes the company, country and scaleserp api key then output the result of thr query """
  # the link to the scale url which then loads the api and format it as a document
  loader = WebBaseLoader(f'https://api.scaleserp.com/search?api_key={api_key}&q={company}&location={country}')
  data = loader.load()
  # this is used to split the document into chunks of text
  text_splitter = RecursiveCharacterTextSplitter(
      chunk_size = 1000,
      chunk_overlap  = 0,
      # length_function = len,
  )
  splitted_documents = text_splitter.split_documents(data)
  # we are using open ai embedding to create embedding
  embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
  # creating a db of the embeddings
  docsearch = Chroma.from_documents(splitted_documents, embeddings)
  llm = OpenAI(temperature=0)
  # the chain from langchain for question and answer
  chain = RetrievalQA.from_chain_type(
          llm=llm,
          chain_type="stuff",
          retriever=docsearch.as_retriever(),
          chain_type_kwargs={"verbose": False},
      )
  # URMMM  look at this prompt and see if you can help out
  question = ["i want you to give me a brief overview of the company ",
  "What are the main products or services associated with the company",
  "the keywords particular to the company, return 'empty' if can't be found",
  "the company's picture, return 'empty' if can't be found",
  "the company location or address, return 'empty' if can't be found",]
  result = chain.apply(question)
  data = output_value(result)
  return data