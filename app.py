import streamlit as st
import re
import os
import chromadb
import urllib.request
import json

# Configure the look of our web page
st.set_page_config(page_title="Secure AI Gateway", page_icon="🔒", layout="centered")
st.title("🔒 Secure Enterprise AI Portal")
st.write("This application filters prompts, blocks injection attacks, and searches corporate documentation 100% locally.")

# Automatically load the library database behind the scenes
@st.cache_resource
def initialize_web_db():
    client = chromadb.Client()
    lib = client.create_collection(name="web_records")
    if os.path.exists("company_policy.txt"):
        with open("company_policy.txt", "r") as f:
            lines = f.readlines()
        lib.add(documents=[l.strip() for l in lines if l.strip()], ids=[f"id_{i}" for i in range(len(lines))])
    return lib

try:
    library = initialize_web_db()
except Exception:
    pass

# Create an interactive text input box for users
user_query = st.text_input("Enter your employee query below:", "Hey, my email is admin@company.ae. Can you look up the rule for accessing servers remotely?")

# Action button
if st.button("Submit Secure Request"):
    # --- PHASE 1: THE SECURITY GATE ---
    bad_words = ["ignore rules", "override", "system prompt", "forget rules"]
    is_attack = any(word in user_query.lower() for word in bad_words)
    
    if is_attack:
        st.error("🚨 SECURITY BLOCKED: Malicious keyword / Prompt Injection attempt detected!")
    else:
        # Clean emails
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        sanitized_query = re.sub(email_pattern, "[HIDDEN_EMAIL]", user_query)
        
        # Display the security action visually on screen
        st.info(f"🛡️ **Guardroom Action:** Prompt sanitized to: *'{sanitized_query}'*")
        
        # --- PHASE 2: THE LIBRARY SEARCH ---
        try:
            search_results = library.query(query_texts=[sanitized_query], n_results=2)
            retrieved_context = search_results['documents']
            st.success(f"📚 **Library Extracted Trusted Context:** {retrieved_context}")
            
            # --- PHASE 3: THE LOCAL AI BRAIN ---
            st.write("🧠 *Querying Local Llama 3.2 Brain over network...*")
            url = "http://localhost:11434/api/generate"
            system_prompt = f"You are a secure corporate assistant. Answer using ONLY this context: {retrieved_context}. If you don't know, refuse to answer."
            
            payload = {
                "model": "llama3.2:1b",
                "prompt": f"Context: {retrieved_context}\nQuestion: {sanitized_query}\nAnswer:",
                "system": system_prompt,
                "stream": False
            }
            
            # Contact Ollama app
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                
                # Display the beautiful AI answer response box
                st.subheader("🤖 Secure AI Response Output:")
                st.write(res_data['response'])
                
        except Exception:
            st.error("❌ Connection Error: Please make sure the Ollama desktop app is running in the background!")
