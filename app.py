import streamlit as st
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from google import genai
from google.genai import types
from openai import OpenAI
from anthropic import Anthropic

st.set_page_config(page_title="AI VoIP Support Co-Pilot", page_icon="🎧", layout="wide")

# --- 1. LOAD & CHUNK KNOWLEDGE BASE ---
@st.cache_data
def load_knowledge_base(filepath="knowledge_base.md"):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    chunks = [chunk.strip() for chunk in text.split("## ") if chunk.strip()]
    return ["## " + chunk for chunk in chunks]

chunks = load_knowledge_base()
vectorizer = TfidfVectorizer(stop_words="english")
chunk_vectors = vectorizer.fit_transform(chunks)

def retrieve_docs(query, top_k=2):
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, chunk_vectors).flatten()
    top_indices = np.argsort(similarities)[::-1][:top_k]
    results = []
    for idx in top_indices:
        if similarities[idx] > 0.05:
            results.append((chunks[idx], round(float(similarities[idx]), 3)))
    return results

# --- 2. LLM GENERATION ---
SYSTEM_PROMPT = """You are a Senior Technical Support Engineer specializing in VoIP, cloud telephony, networking, and SaaS integrations.
Use ONLY the provided Knowledge Base context to answer the support agent's query.
Format your response clearly into three sections:
1. **Likely Root Cause**
2. **Step-by-Step Troubleshooting Checklist**
3. **Draft Customer Reply** (empathetic, concise, and clear for a non-technical end user)

If the provided context does not cover the issue, state clearly: "This issue is not covered in the current Knowledge Base. Gather Call-ID, timestamp, and network logs, and escalate to Tier-2 Engineering." Do not invent technical steps."""

def generate_answer(provider, api_key, user_query, retrieved_context):
    user_message = f"KNOWLEDGE BASE CONTEXT:\n{retrieved_context}\n\nSUPPORT TICKET / ISSUE:\n{user_query}"
    
    if provider == "Google Gemini (Free Tier)":
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.2,
            ),
        )
        return response.text
    elif provider == "OpenAI (GPT-4o-mini)":
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content
    else:
        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-3-5-haiku-latest",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
            temperature=0.2
        )
        return response.content[0].text

# --- 3. STREAMLIT UI ---
st.title("🎧 AI VoIP & Telephony Troubleshooting Co-Pilot (RAG)")
st.markdown("Retrieve internal troubleshooting SOPs, diagnose SIP/RTP network issues, and generate customer-ready responses.")

with st.sidebar:
    st.header("⚙️ Model Configuration")
    provider = st.selectbox(
        "Select AI Provider",
        ["Google Gemini (Free Tier)", "OpenAI (GPT-4o-mini)", "Anthropic (Claude 3.5 Haiku)"]
    )
    provider_label = provider.split(" ")[0]
    api_key = st.text_input(f"Enter your {provider_label} API Key", type="password")
    st.divider()
    st.markdown("**Sample Test Queries:**")
    st.caption("• Customers say they can hear us, but we can't hear them on outbound calls.")
    st.caption("• Desk phones show 403 Forbidden error after ISP router replacement.")
    st.caption("• CRM screen-pop is delayed by 2 minutes after calls end.")

query = st.text_area("Describe the customer issue or paste the support ticket:", height=100, placeholder="e.g., Clinic reports robotic audio and dropped calls every afternoon...")

if st.button("Diagnose & Generate Response", type="primary"):
    if not api_key:
        st.error("Please enter your API key in the sidebar first.")
    elif not query.strip():
        st.warning("Please enter a support issue to troubleshoot.")
    else:
        with st.spinner("Searching Knowledge Base and generating troubleshooting steps..."):
            retrieved = retrieve_docs(query)
            
            col1, col2 = st.columns([3, 2])
            with col1:
                st.subheader("🛠️ AI Troubleshooting & Response")
                if not retrieved:
                    st.warning("No matching KB article found. Recommend escalating to Tier-2 with Call-ID and network logs.")
                else:
                    context_text = "\n\n---\n\n".join([doc for doc, _ in retrieved])
                    try:
                        answer = generate_answer(provider, api_key, query, context_text)
                        st.markdown(answer)
                    except Exception as e:
                        st.error(f"API Error: {e}")
            
            with col2:
                st.subheader("📚 Retrieved KB Sources")
                if retrieved:
                    for doc, score in retrieved:
                        title = doc.splitlines()[0].replace("## ", "")
                        with st.expander(f"{title} (Match: {score})", expanded=True):
                            st.markdown(doc)
                else:
                    st.info("0 relevant articles matched.")
