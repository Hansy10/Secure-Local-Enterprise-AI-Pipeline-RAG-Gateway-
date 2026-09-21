import re
import os
import chromadb
import urllib.request
import json

print("🔒 AI Security, Library & Brain Pipeline Booting Up...")

# =========================================================
# STEP 1: THE SECURITY GUARDROOM (Scrub PII & Block Attacks)
# =========================================================
def clean_and_check(user_text):
    # Stop common hacker injection phrases
    bad_words = ["ignore rules", "override", "system prompt", "forget rules"]
    for word in bad_words:
        if word in user_text.lower():
            raise ValueError("🚨 BLOCKED: Potential hacker attack detected!")
            
    # Automatically scrub out email patterns
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.sub(email_pattern, "[HIDDEN_EMAIL]", user_text)

# =========================================================
# STEP 2: THE LOCAL LIBRARY (The Private RAG Database)
# =========================================================
db_client = chromadb.Client()
library = db_client.create_collection(name="company_records")

if os.path.exists("company_policy.txt"):
    with open("company_policy.txt", "r") as f:
        policies = f.readlines()
    library.add(
        documents=[p.strip() for p in policies if p.strip()],
        ids=["doc1", "doc2"]
    )
    print("📚 Private library loaded successfully into memory!")
else:
    print("❌ Error: company_policy.txt not found in this folder.")

# =========================================================
# STEP 3: THE AI BRAIN LAYER (Connecting to your Local Ollama)
# =========================================================
def ask_local_ai(context_document, safe_question):
    url = "http://localhost:11434/api/generate"
    
    # Establish hard rules for the local Llama model
    system_prompt = f"You are a secure assistant. Answer using ONLY this context: {context_document}. If you don't know, say 'Unauthorized Request'."
    
    data = {
        "model": "llama3.2:1b",
        "prompt": f"Context: {context_document}\nQuestion: {safe_question}\nAnswer:",
        "system": system_prompt,
        "stream": False
    }
    
    # Send the safe query over to your Ollama application engine
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data['response']
    except Exception:
        return "❌ Error: Could not connect to Ollama. Make sure the Ollama desktop app is open!"

# =========================================================
# RUNNING THE PIPELINE
# =========================================================
employee_query = "Hey, my email is admin@company.ae. Can you look up the rule for accessing servers remotely?"
print(f"\n[Employee Asks]: {employee_query}")

try:
    # A. Clean data first
    safe_query = clean_and_check(employee_query)
    print(f"1. 🛡️ Security Gate: Sanitized query to: '{safe_query}'")
    
    # B. Fetch the exact truth from your files
    search_results = library.query(query_texts=[safe_query], n_results=2)
    retrieved_fact = search_results['documents'][0]
    print(f"2. 📚 Library Search Extracted: \"{retrieved_fact}\"")
    
    # C. Hand safe question and trusted fact to the model
    print("3. 🧠 Querying Local Llama 3.2 Brain...")
    ai_response = ask_local_ai(retrieved_fact, safe_query)
    
    print("\n🤖 [Secure AI Answer Output]:")
    print(ai_response)

except ValueError as e:
    print(e)
