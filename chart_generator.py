import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
import base64

def generate_chart(data, chart_config):
    try:
        if isinstance(data, dict):
            data = [data]
        elif not isinstance(data, list):
            return {"error": "Unsupported data format for charting."}

        if not all(isinstance(item, dict) for item in data):
            return {"error": "Each item in the data list must be a dictionary."}

        df = pd.DataFrame(data)

        x = chart_config.get("xlabel", "timestamp")
        y = chart_config.get("ylabel", "temperature")
        title = chart_config.get("title", "Generated Chart")

        if x not in df.columns or y not in df.columns:
            return {
                "error": f"Could not find suitable x ({x}) or y ({y}) column in data."
            }

        df = df.sort_values(by=x)

        plt.figure(figsize=(10, 5))
        plt.plot(df[x], df[y], marker="o")
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(title)
        plt.grid(True)

        buf = BytesIO()
        plt.savefig(buf, format="png")
        plt.close()
        buf.seek(0)
        return {"chart_base64": base64.b64encode(buf.read()).decode("utf-8")}

    except Exception as e:
        return {"error": str(e)}
