# 🎧 AI VoIP & Telephony Troubleshooting Co-Pilot (RAG)

A Retrieval-Augmented Generation (RAG) support assistant built to accelerate Tier-1 and Tier-2 troubleshooting for cloud telephony, SIP/RTP networking, and CRM webhook integrations.

## 🚀 Problem Solved
Technical support specialists often lose valuable time digging through scattered Standard Operating Procedures (SOPs) while customers wait with live call-quality or registration issues. General-purpose AI chatbots often invent or "hallucinate" inaccurate networking steps, making them unsafe for customer-facing environments. 

This application solves both challenges by retrieving verified internal troubleshooting documentation and generating three structured outputs:
1. **Likely Root Cause**
2. **Step-by-Step Troubleshooting & Escalation Checklist**
3. **Empathetic, Non-Technical Customer Reply**

## 🛠️ Tech Stack
- **Frontend & UI:** Streamlit (Python)
- **Retrieval Engine:** Scikit-Learn (`TfidfVectorizer` & Cosine Similarity)
- **LLMs Supported:** Google Gemini (`gemini-3.5-flash-lite`), OpenAI (`gpt-4o-mini`), and Anthropic (`claude-3-5-haiku`)
- **Domain Coverage:** SIP Signaling (`401`/`403`/`408` errors), Symmetric NAT & SIP ALG, RTP Media Ports (`UDP 10000–20000`), STUN/ICE, QoS/Jitter, and CRM OAuth Webhooks

## ✨ Key Features
- **Grounded Retrieval with Source Transparency:** Displays matched Knowledge Base articles alongside similarity match scores so agents can verify every recommendation.
- **Anti-Hallucination Guardrails:** Strictly instructed to rely only on retrieved documentation and trigger Tier-2 engineering escalation protocols (gathering `Call-ID`, timestamps, and PCAP/MTR logs) when an issue falls outside documented SOPs.
- **Multi-LLM Provider Architecture:** Supports seamless switching between Google Gemini, OpenAI, and Anthropic APIs with runtime API key input for secure, stateless execution.

## 💻 How to Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com
   cd voip-support-rag-copilot
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch the Streamlit web app:
   ```bash
   streamlit run app.py
   ```
4. Enter your Google AI Studio (Gemini), OpenAI, or Anthropic API key in the sidebar and test with any VoIP or CRM webhook issue.
