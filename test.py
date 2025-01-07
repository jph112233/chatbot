# Conversational Retrieval QA Chatbot, built using Langflow and Streamlit
# Author: Gary A. Stafford
# Date: 2023-07-28
# Usage: streamlit run streamlit_app.py
# Requirements: pip install streamlit streamlit_chat -Uq

import logging
import sys
import time
from typing import Optional
import requests
import streamlit as st
from streamlit_chat import message

output_type: str = "chat",
input_type: str = "chat",

log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=log_format, stream=sys.stdout, level=logging.INFO)

BASE_API_URL = "https://api.langflow.astra.datastax.com"
FLOW_ID = "dee04a52-3bb8-415a-86b5-25e7aee846e5"
APPLICATION_TOKEN ="AstraCS:LSQvFBjPCbaPPMSWRmameeDv:fbd2b1611eda0ba8cd7d1787fd674e4b146326bb5e0b0e07272d7fb5ada41ecd"

# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
TWEAKS = {
  "OpenAIEmbeddings-3OTU2": {},
  "Chroma-elGpI": {},
  "ChatOpenAI-38h1l": {"model_name": "gpt-4"},
  "ConversationalRetrievalChain-4FTbi": {},
  "ConversationBufferMemory-YTFcZ": {}
}
BASE_AVATAR_URL = (
    "https://raw.githubusercontent.com/garystafford-aws/static-assets/main/static"
)

api_url = f"{BASE_API_URL}/{FLOW_ID}"



#    if tweaks:
#        payload["tweaks"] = tweaks

payload = {
        "input_value": "who is paul",
        "output_type": output_type,
        "input_type": input_type,
}
logging.info(f"payload:   {payload}")
logging.info(f"Tweaks:   {TWEAKS}")

payload["tweaks"] = TWEAKS
logging.info(f"payload:   {payload}")


api_url="https://api.langflow.astra.datastax.com/lf/08ff40ee-0309-4857-a339-6136a9b9a604/api/v1/run/dee04a52-3bb8-415a-86b5-25e7aee846e5?stream=false"
### Add authentication header=
headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
response = requests.post(api_url, json=payload, headers=headers)
logging.info(f"response:   {response}")



def run_flow(inputs: dict, flow_id: str, tweaks: Optional[dict] = None) -> dict:

    return response.json()
    


def generate_response(prompt):
    logging.info(f"question: {prompt}")
    inputs = {"question": prompt}
    response = run_flow(inputs, flow_id=FLOW_ID, tweaks=TWEAKS)
    try:
        logging.info(f"answer: {response['result']['answer']}")
        return response["result"]["answer"]
    except Exception as exc:
        logging.error(f"error: {response}")
        return "Sorry, there was a problem finding an answer for you."


