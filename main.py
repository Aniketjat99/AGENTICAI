from tavily import TavilyClient
import os
from dotenv import load_dotenv
from transformers import pipeline

load_dotenv()

# Tavily setup
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# ✅ FIXED: correct free model
summarizer = pipeline("text-generation", model="google/flan-t5-base")

# Input
query = input("Enter topic: ")

# Step 1: Search
response = tavily.search(query=query, max_results=3)
data = " ".join([r["content"] for r in response["results"]])

# Step 2: Summarize (FIXED)
summary = summarizer(
    "Summarize this: " + data[:1000],
    max_new_tokens=150,
    do_sample=False
)

result = summary[0]['generated_text']

# Remove "Summarize this:" if present
result = result.replace("Summarize this:", "").strip()
# Step 3: Save
os.makedirs("output", exist_ok=True)  # folder auto create
with open("output/report.txt", "w", encoding="utf-8") as f:
    f.write(result)

print("\n✅ Result:\n")
print(result)