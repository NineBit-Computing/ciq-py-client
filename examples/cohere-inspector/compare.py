import os
import json
import sys
import fitz

from ninebit_ciq import NineBitCIQClient
from cohere import Client as CohereClient

api_key = os.getenv("API_KEY") or ""
cohere_api_key = os.getenv("COHERE_API_KEY") or ""

try:
    ciq_client = NineBitCIQClient(api_key=api_key)
    cohere_client = CohereClient(cohere_api_key)
except Exception as e:
    print(f"Error while setting up CIQ client {e}")
    sys.exit(1)

# step 1: Extract text from PDF and generate a question

pdf_path = "examples/core-sanity/geo_chap_9.pdf"


def extract_pdf_text(path):
    with fitz.open(path) as doc:
        text = ""
        for page in doc:
            page_text = page.get_text().strip()
            text += page_text + "\n"
        return text.strip()


def get_limited_context(text, char_limit=25000):
    return text[:char_limit].strip()


full_text = extract_pdf_text(pdf_path)

combined_context = get_limited_context(full_text)
# print("📄 Full PDF Text Extracted", combined_context)
question_prompt = f"""
You are a teacher preparing a comprehension question based on the document below.

📄 Document Content:
{combined_context}

Generate **one meaningful and specific question** that tests understanding of this content.
Only return the question, nothing else.
"""

question_response = cohere_client.generate(
    prompt=question_prompt, max_tokens=50, temperature=0.5, model="command-r-plus"
)

query = question_response.generations[0].text.strip()
print("❓ Auto-Generated Question:", query)

# Step 2: CIQ Ingest PDF and Query


def on_done(error, data):
    if error:
        print(f"❌ Ingest failed: {error}")
    else:
        print(f"✅ Ingest succeeded: {data}")


ciq_client.ingest_file(file=pdf_path, callback=on_done)

ciq_answer = ciq_client.rag_query(query=query)
print("\n🔷 CIQ Answer:\n", ciq_answer)

# Step 3: Cohere Chat and Evaluation

evaluation_prompt = f"""
You are an expert evaluator and assistant.

🔹 Task 1: Evaluate the following answer
Question:
{query}

CIQ's Answer:
{ciq_answer}

Based on the document content below, evaluate the CIQ answer on the following criteria:
- ✅ Accuracy (Is it factually correct?)
- ✅ Completeness (Did it cover all relevant information?)
- ✅ Clarity (Is it clearly and precisely worded?)

Provide a score from 1 to 10 and explain your reasoning in a few sentences.

🔹 Task 2: Generate your own answer
Now, based ONLY on the document content below, write your own answer to the same question.

📄 Document Content:
{combined_context}

---
Return the result as a JSON object with the following format:
{{
  "evaluation": "<your evaluation here>",
  "score": "<number between 1 and 10>",
  "cohere_answer": "<your generated answer here>"
}}
"""

cohere_judge = cohere_client.generate(prompt=evaluation_prompt, max_tokens=300, temperature=0.3, model="command-r-plus")
cohere_judge_text = cohere_judge.generations[0].text.strip()

# print("\n🧑‍⚖️ Cohere's Evaluation:\n", )


try:
    coehre_evaluation = json.loads(cohere_judge_text)
    results = {
        "cohere_generated_question": query,
        "ciq_generated_answer": ciq_answer,
        "ciq_answer_evaluation": coehre_evaluation["evaluation"],
        "ciq_answer_score": coehre_evaluation["score"],
        "cohere_generated_answer": coehre_evaluation["cohere_answer"],
    }

    # Print for logs
    print("\n 🧑‍⚖️ Evaluation Results:")
    for key, value in results.items():
        print(f"{key}: {value}")

    # Save to JSON file
    with open("report.json", "w") as f:
        json.dump(results, f, indent=2)
except json.JSONDecodeError:
    print("Response is not valid JSON. Raw output:")
    print(cohere_judge_text)
    sys.exit(1)
