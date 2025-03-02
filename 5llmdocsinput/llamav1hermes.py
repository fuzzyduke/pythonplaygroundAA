import logging
logging.basicConfig(level=logging.DEBUG)

from langchain_community.llms import GPT4All

llm = GPT4All(model="D:/hermes3llama3/H3Ll323BQ4KM.gguf", backend="cpu")
response = llm.invoke("Who won the FIFA World Cup in 2022?")
print(response)
