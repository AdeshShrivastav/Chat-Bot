import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage,AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain import hub
from langchain.agents import load_tools
from tempfile import TemporaryDirectory

from langchain_community.agent_toolkits import FileManagementToolkit
working_directory = TemporaryDirectory()


search = DuckDuckGoSearchRun()
res = search.run("who won ipl 2025")
print(res)
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())



file = FileManagementToolkit(
    root_dir=str(working_directory.name),
    selected_tools=["read_file", "write_file", "list_directory"],
).get_tools()

tools = [search,wikipedia]
import os

# page Config
st.set_page_config(
    page_title="QA bot",
    page_icon="rocket"
)
st.title("Adesh's Bot")

with st.sidebar:
    st.header('Settings')

    ##API_key
    api_key = st.text_input("GOOGLE_API_KEY",type="password",help= "get Api key from Google studio")


    ##Model selection
    modelname = st.selectbox(
        "Model",
        ["gemini-2.5-flash"],
        index= 0
    )
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Set up the LangChain memory
msgs = StreamlitChatMessageHistory()
if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you?")

## Inisialize LLM

@st.cache_resource
def get_chain (api_key,model_name):
    if not api_key:
        return None
    
  
    os.environ["GOOGLE_API_KEY"] = api_key

    llm = init_chat_model(model_name, model_provider="google_genai")
    llm2 = llm.bind_tools(tools)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system","You are Adesh Bot A helpful assistent.Answer questions clearly and conciesly"),
            MessagesPlaceholder(variable_name="history"),
            ("user","{question}")
        ]
    )

    ## create Chain
    chain = prompt | llm | StrOutputParser()
    chain_with_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: msgs,
        input_messages_key="question",
        history_messages_key="history",
    )

    return chain_with_history


# """Inisialize duckduckgo chain"""

@st.cache_resource
def get_chain2 (api_key,model_name):
    if not api_key:
        return None
    
    # inisialize groq model
    os.environ["GOOGLE_API_KEY"] = api_key

    llm = init_chat_model(model_name, model_provider="google_genai")
    llm2 = llm.bind_tools(tools)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system","You are Adesh Bot A helpful assistent.Answer questions clearly and conciesly"),
            MessagesPlaceholder(variable_name="history"),
            ("user","{question}")
        ]
    )

    ## create Chain

    chain = prompt | llm2 | StrOutputParser()
    chain_with_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: msgs,
        input_messages_key="question",
        history_messages_key="history",
    )

    return chain_with_history

chain2 = get_chain2(api_key,modelname)

chain= get_chain(api_key,modelname)
if not chain :
    st.warning("Please enter your API key in the sidebar")

else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message['content'])


## Chatinput 

if question:= st.chat_input("Ask me anything"):
    st.session_state.messages.append({"role":"user","content":question})

    with st.chat_message("user"):
        st.write(question)



    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        full_responce = ""

        try:
            for chunk in chain2.stream({"question":question,"history":msgs.messages}, config={"configurable": {"session_id": "foo"}}):
                full_responce += chunk
                message_placeholder.markdown(full_responce + " ")

            st.session_state.messages.append(
                {"role":"assistant",
                 "content":full_responce}
            )

            if full_responce == "":

                for chunk in chain.stream({"question":question,"history":msgs.messages}, config={"configurable": {"session_id": "foo"}}):
                    full_responce += chunk
                    message_placeholder.markdown(full_responce + " ")

                st.session_state.messages.append(
                    {"role":"assistant",
                    "content":full_responce}
                )

        except Exception as e:
            st.error(f"Error : {str(e)}")
