#  Task 4: Automation Orchestrator – AI Merch Maker Lite

This module automates the AI Merch Maker pipeline by:
1. Generating a fun T-shirt product using Google's Gemini 1.5 Flash model.
2. Sending the product to a local fake publisher API for publishing.

Built with **Python** and **Streamlit**, this orchestrator can be run manually and simulates the daily product generation and publishing workflow.

---

##  Features

-  Uses Gemini 1.5 Flash (free model) to generate T-shirt product data.
-  Sends generated product to a fake publishing API (`http://localhost:8000`).
-  Includes retry logic if Gemini is temporarily overloaded (503 error).
-  Comes with a user-friendly Streamlit interface.
-  API key management via `.env` file.

---

##  How to Run

### 1. Clone the repo or navigate to the `automation_orchestrator` folder

```bash
cd AI-Merch-Maker-Lite/automation_orchestrator

https://naser-test-store.myshopify.com/admin/products
