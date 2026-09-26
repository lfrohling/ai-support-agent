# ai-support-agent

# 🤖 AI-Powered Customer Support Triage & Lead Routing Agent : Website Edition

A live, production-grade microservice designed to automate enterprise communication workflows. This tool analyzes incoming customer emails, reviews, or sales inquiries, extracts structured operational metadata, and auto-drafts highly contextualized executive responses in real-time.

🌍 **Live Demo:** (https://luke-frohling-ai-support-agent.streamlit.app/)

## 💼 Business Value Case
Manual support ticket triage costs businesses millions in lost productivity and slow customer response times. This solution addresses those structural bottlenecks by:
* **Reducing Response Latency:** Automatically flags urgent accounts or cancellation risks for immediate human intervention.
* **Smart Data Extraction:** Converts chaotic, unstructured text strings into reliable, parsable JSON data payloads.
* **Automated Scaling:** Routes requests directly to Billing, Tech Support, or Sales departments without human triage overhead.

## 🛠️ Tech Stack & Architecture
* **Frontend UI Framework:** Streamlit (Hosted on Streamlit Community Cloud)
* **AI Core Backend:** Google Gemini API SDK (`gemini-3.8-flash`)
* **Language:** Python 3.12
* **Data Format:** Structured JSON Output

## In case of large traffic 
Activate the "simulated" toggle option.

## To test this application 
Give it something to work on... for example enter in a typical customer complaint to see how to algorithm handles the data... 
"Hi, I love your app but my billing department just noticed we were charged twice for our enterprise subscription this month. Please fix this immediately or we will have to cancel our contract. Thanks, Luke from Amazon."
