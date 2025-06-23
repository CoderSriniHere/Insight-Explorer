# Insight-Explorer
# 🔍 AI-Powered Time-Series Insight Explorer

An intelligent system that allows users to ask natural language questions about time-series data (like temperature, voltage, CO₂ levels, etc.) and get **instant answers, insights, and beautiful charts** — all powered by LLMs and FastAPI. 🧠📊

---

## 🚀 Features

- 🧠 **Natural Language Querying**
  - Ask questions like:  
    - `"Show temperature over time"`  
    - `"List entries with voltage below 220 volts"`  
    - `"Plot current levels by timestamp"`

- 📊 **Visual Chart Generation**
  - Auto-plots line graphs using `matplotlib` based on query results

- 📦 **Backend with FastAPI**
  - Processes natural queries, runs MongoDB queries, and returns structured responses

- 🖥️ **Streamlit Frontend**
  - Interactive, user-friendly UI to type your query and view chart + summary

- 🧪 **Mock Fallback System**
  - If Groq API fails, a built-in fallback returns mock query structures to ensure smooth demo or offline usage

---

## 🧰 Tech Stack

| Layer         | Tech Used                         |
|---------------|-----------------------------------|
| LLM           | [Groq](https://console.groq.com/) (LLaMA 3 70B via API) |
| Backend API   | [FastAPI](https://fastapi.tiangolo.com/) |
| Frontend      | [Streamlit](https://streamlit.io/) |
| Database      | [MongoDB](https://www.mongodb.com/) |
| Charting      | `matplotlib`, `pandas`            |
| Data Format   | JSON                              |

---

## 📂 Project Structure
ai_insight_app/
├── main.py # FastAPI backend
├── streamlit_app.py # Streamlit frontend
├── query_handler.py # Core NLP + DB handler
├── chart_generator.py # Matplotlib chart renderer
├── groq_helper.py # Groq + fallback logic
├── sample_data_generator.py # Generate 3 weeks of data
├── .env.example # Example environment config
├── requirements.txt # Python dependencies
