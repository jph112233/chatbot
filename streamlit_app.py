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

log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=log_format, stream=sys.stdout, level=logging.INFO)


# Get query parameters from the URL.
query_params = st.query_params

# Access specific parameters
# If URL is "/?name=John&age=25"
sitename = query_params.get("site", "").lower()  # Returns "John"
match sitename:
    case "attic":
        #st.write("Name equals John")
        strSiteName="attic"
        strImage="https://www.atticbreeze.net/AB_webstore/squirrelcart/themes/ab-v5/images/store_logo.png"
        strTitle="Attic Breeze"
        FLOW_ID = st.secrets["flow_id_attic"]
    case "tess":
        strSiteName="tess"
        strImage="https://yt3.googleusercontent.com/ZVwaBIidQtbCYGmGeanRD2J7ik_srsXgvXUlkEOGIZZDoczmsrHWXiihUzcKoMmTXWMoSbs=w2276-fcrop64=1,00005a57ffffa5a8-k-c0xffffffff-no-nd-rj"
        FLOW_ID = st.secrets["flow_id_tess"]
        strTitle="Tess Oral Health"
    case "canariis":
        strSiteName="canariis"
        strImage="https://canariis.com/App_Themes/Canariis/Images/logo.jpg"
        FLOW_ID = st.secrets["flow_id_canariis"]
        strTitle="Canariis"
    case "ams":
        strSiteName="ams"
        strImage="https://www.govmint.com/media/logo/stores/1/GovMint-Logo-Sub.png"
        FLOW_ID = st.secrets["flow_id_ams"]
        strTitle="AMS"
    case _:
        st.write("Name not recognized")

BASE_API_URL = st.secrets["base_api_url"]
LANGFLOW_ID = st.secrets["langflow_id"]

APPLICATION_TOKEN = st.secrets["application_token"]
# FlowID, Image




# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
TWEAKS = {
#    "ChatInput-px7mJ": {},
#    "ParseData-iCfxn": {},
#    "Prompt-uxud0": {},
#    "SplitText-p1gJK": {},
#    "OpenAIModel-FhydA": {},
#    "ChatOutput-9FRtl": {}
}
BASE_AVATAR_URL = (
    "https://raw.githubusercontent.com/garystafford-aws/static-assets/main/static"
)


def main():
    st.set_page_config(page_title=strTitle)
    


    st.image(strImage)
    st.write("")  # Adds a blank line
    st.write("")  # Adds a blank line
    st.markdown("##### Welcome!")
    


    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message["avatar"]):
            st.write(message["content"])

    if prompt := st.chat_input("What can we help with?"):
        # Add user message to chat history
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
                "avatar": f"{BASE_AVATAR_URL}/people-64px.png",
            }
        )
        # Display user message in chat message container
        with st.chat_message(
            "user",
            avatar=f"{BASE_AVATAR_URL}/people-64px.png",
        ):
            st.write(prompt)

        # Display assistant response in chat message container
        with st.chat_message(
            "assistant",
            avatar=f"{BASE_AVATAR_URL}/bartender-64px.png",
        ):
            message_placeholder = st.empty()
            with st.spinner(text="Thinking..."):
                assistant_response = generate_response(prompt)
                message_placeholder.write(assistant_response)
        # Add assistant response to chat history
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_response,
                "avatar": f"{BASE_AVATAR_URL}/bartender-64px.png",
            }
        )


def run_flow(inputs: dict, flow_id: str, tweaks: Optional[dict] = None) -> dict:
    #api_url = f"{BASE_API_URL}/{flow_id}"
    api_url=f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{FLOW_ID}"
#    payload = {"inputs": inputs}
    payload = {
        "input_value":  inputs ['question'],
        "output_type": "chat",
        "input_type": "chat",
    }
    if tweaks:
        payload["tweaks"] = tweaks

### Add authentication header=
    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
    # Add debug logging
    logging.info(f"API URL: {api_url}")
    logging.info(f"Payload: {payload}")
    logging.info(f"Headers: {headers}")

    response = requests.post(api_url, json=payload, headers=headers)
    # Add response debugging
    logging.info(f"Response Status Code: {response.status_code}")
    logging.info(f"Response Headers: {response.headers}")
    logging.info(f"Response Content: {response.text}")
    

    return response.json()


def generate_response(prompt):
    logging.info(f"question: {prompt}")
    inputs = {"question": prompt}
    response = run_flow(inputs, flow_id=FLOW_ID, tweaks=TWEAKS)
    try:
#        logging.info(f"answer: {response['result']['answer']}")
#        return response["result"]["answer"]
#        st.write(response)  
#        st.write(response['outputs'][0]['outputs'][0]['results']['message']['data']['text'])
#        return response ['outputs'][0]['outputs'][0]['results']['message']['text']
        message_text =  response['outputs'][0]['outputs'][0]['results']['message']['data']['text']
        logging.info(f"answer: {message_text}")
        return message_text

    except requests.exceptions.RequestException as e:
        logging.error(f"API request error: {e}")
        return "Sorry, there was a problem connecting to the service."
    except (KeyError, IndexError) as e:
        logging.error(f"Response parsing error: {e}")
        logging.error(f"Response structure: {response}")
        return "Sorry, there was a problem processing the response."
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return "Sorry, an unexpected error occurred."

    except Exception as exc:
        logging.error(f"error: {response}")
        return "Sorry, there was a problem finding an answer for you."


if __name__ == "__main__":
    main()