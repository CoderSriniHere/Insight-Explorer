import streamlit as st
import requests
import base64
import pandas as pd

st.set_page_config(page_title="AI Insight Explorer", layout="wide")

st.title("🤖 AI-Powered Time-Series Insight Explorer")
st.write("Ask questions about your data in plain English!")

nl_query = st.text_input("🔍 Enter your natural language query:")

if st.button("Submit") and nl_query:
    with st.spinner("🧠 Thinking..."):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/query",
                json={"query": nl_query}
            )
            result = response.json()

            # If chart response
            if "chart_base64" in result:
                st.subheader("📊 Chart")
                st.image(base64.b64decode(result["chart_base64"]), use_column_width=True)
                st.success("✅ Here's the chart generated based on your query.")

            # If structured documents response
            elif "documents" in result:
                docs = result["documents"]
                st.subheader("📄 Query Results")
                st.success(f"📝 {result['response']}")
                # Display as DataFrame if possible
                try:
                    df = pd.DataFrame(docs)
                    st.dataframe(df)
                except Exception:
                    st.json(docs)

            # If plain message
            elif "response" in result:
                st.success(result["response"])

            # If error
            elif "error" in result:
                st.error(f"❌ Error: {result['error']}")

            else:
                st.warning("❌ Unknown response format received.")

        except Exception as e:
            st.error(f"⚠️ Request failed: {e}")
