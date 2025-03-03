from langchain_community.llms import GPT4All
from browser_use import Agent  # Correct import
import browser_use

print(dir(browser_use))  # Debugging: List available objects

# Define LLM path
llm_path = "D:/hermes3llama3/H3Ll323BQ4KM.gguf"

# Load Local LLM
llm = GPT4All(model=llm_path)

# Initialize Browser Agent (Providing required arguments)
browser = Agent(task="search", llm=llm)  # ✅ Corrected

# Function to interact with LLM
def ask_llm(question):
    response = llm.invoke(question)
    return response.strip()

# Example: AI agent researching & summarizing Twitter posts
query = "Summarize the latest tweets about AI automation"
search_results = browser.search_google(query)  # ✅ Use Agent for web search
llm_response = ask_llm(f"Summarize this info: {search_results}")

print("🔹 AI Summary:", llm_response)
