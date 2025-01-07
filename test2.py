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


payload = {
    "input_value": "give me 2 words to describe paul",
    "output_type": "chat",
    "input_type": "chat",
    "tweaks": {
        "ChatInput-px7mJ": {},
        "ParseData-iCfxn": {},
        "Prompt-uxud0": {},
        "SplitText-p1gJK": {},
        "OpenAIModel-FhydA": {},
        "ChatOutput-9FRtl": {}
    }
}







logging.info(f"payload:   {payload}")


api_url="https://api.langflow.astra.datastax.com/lf/08ff40ee-0309-4857-a339-6136a9b9a604/api/v1/run/dee04a52-3bb8-415a-86b5-25e7aee846e5?stream=false"
### Add authentication header=
headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
response = requests.post(api_url, json=payload, headers=headers)
logging.info(f"response:   {response}")
response_json = response.json()

logging.info(f"response:   {response_json}")

message_text = response_json['outputs'][0]['outputs'][0]['results']['message']['text']
logging.info(f"AI Response: {message_text}")  # Will print: "Innovative Leader"


#logging.info(f"answer: {response['outputs': 'inputs']}")

