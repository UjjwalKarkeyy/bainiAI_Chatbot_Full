from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from utils import file_reader, appointment_reader_saver
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.retrievers import MultiQueryRetriever
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage
from datetime import date
import os
import shutil
import warnings
import re

"""
                        Store Current Date for Appointment Booking
-----------------------------------------------------------------------------------------------
"""

curr_date = date.today()

"""
                        Ignoring Warnings for Score
-----------------------------------------------------------------------------------------------
"""
warnings.filterwarnings(
    "ignore",
    message="The method `BaseRetriever.get_relevant_documents` was deprecated in langchain-core 0.1.46 and will be removed in 1.0. Use :meth:`~invoke` instead",
    category=UserWarning
)

"""
                        Load API Key from Environment (.env)
-----------------------------------------------------------------------------------------------
"""
# load api key from .env files
load_dotenv()

"""
                                Load Documents (RAG -> Retrieval)
-----------------------------------------------------------------------------------------------
"""
# path of data
data_path = "./data"

# call file reader from utils.py
# Note: Can contain list of lists
loaded_files = file_reader(path = data_path, extensions=("docx", "pdf"))

"""
                                Create Chunks
-----------------------------------------------------------------------------------------------
"""

def split_text(documents: list[Document]):
    # initialize text splitter with specified parameters
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 300,
        chunk_overlap = 100,
        length_function  = len,
        add_start_index = True,
    )

    # split documents into smaller chunks using text splitter
    chunks = text_splitter.split_documents(documents)
    # print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks

"""
                                Save Documents as Vector Embeddings in Chroma DB
-----------------------------------------------------------------------------------------------
"""

# path to the dir to save chroma db
CHROMA_PATH = "./chroma"
def save_to_chroma(chunks: list[Document]):
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    for chunk in chunks:
        Chroma.from_documents(
            chunk,
            HuggingFaceEmbeddings(
                model_name = "sentence-transformers/all-MiniLM-L6-v2"
            ),
            persist_directory = CHROMA_PATH,
        )
        # print("Chunk saved!")

"""
                Function Calls: Load Documents, Create Chunks, & Save to Chroma DB
-----------------------------------------------------------------------------------------------
"""

def generate_data_store():
    chunks = []
    documents = loaded_files
    for doc in documents:
        chunks.append(split_text(doc))
    save_to_chroma(chunks)

"""
                                RAG -> Augmentation
-----------------------------------------------------------------------------------------------
"""
embedding_function = None
db = None

def load_rag():
    
    # use HuggingFace Embedding Function
    embedding_function = HuggingFaceEmbeddings(
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
    )

    # prepare chroma DB
    return Chroma(
        persist_directory = CHROMA_PATH,
        embedding_function = embedding_function,
    )

"""
            RAG -> Generation + Temporary Chatbot Memory (Using Simple List Append)
-----------------------------------------------------------------------------------------------
"""

def BainiAI(user_input: str):
    # print(user_input)
    # retrive context from the DB using multiquery retriever
    results = multi_retriever.invoke(user_input)
    # check if there are results
    if not results:
        return "Unable to answer that!"

    else:
        # combine context from matching documents
        context_text = "\n\n - - \n\n".join([doc.page_content for doc in results])
        # print(context_text)

        # create prompt template using context and query text
        PROMPT_TEMPLATE = """
            You are BainiAI, the official virtual assistant of TechNova Solutions Pvt. Ltd.  
            You help users with company information, policy-related questions (HR, IT, etc.), and appointment bookings.

            Use the provided context to answer queries.  
            If the answer is not in the context, respond politely that you don’t have that information.

            When handling appointments:
            - Collect: Name, Phone Number, Email, and Preferred Date.
            - Make sure to confirm the details in this exact format (no markdown, symbols, or extra text):

            Name: <full name>
            Phone Number: <digits only>
            Email: <valid email>
            Date: <YYYY-MM-DD>

            Example:
            Name: Ujjwal Karki
            Phone Number: 9824097004
            Email: ujjwalkarki0413@gmail.com
            Date: 2025-11-12

            Always convert relative dates (e.g., “tomorrow,” “next Monday”) into actual calendar dates based on today’s date: {curr_date}.  
            Only after user confirms, finalize with a short response including the words “appointment” and “booked.”

            Context:
            {context}

            Question:
            {question}
        """
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context = context_text, question = user_input, curr_date = curr_date)
        response = conversation.invoke(
            {"messages": [HumanMessage(content=prompt)]},
            config = {"configurable": {"session_id": "default"}},
        )
        return response
    
"""
                                Use Regex to Gain Appointment Details
-----------------------------------------------------------------------------------------------
"""

def appointment_details(ai_msg: str):
    has_appointment = re.search(r"\bappointment[s]?\b", ai_msg, re.IGNORECASE)
    has_booked = re.search(r"\b(book(ed|ing)?)\b", ai_msg, re.IGNORECASE)

    if not (has_appointment and has_booked):
        return None

    # Collect AI messages from chat history (most recent first)
    ai_messages = [m.content for m in reversed(chat_history.messages) if m.type == "ai"]

    # Make sure there are at least 2 AI messages
    if len(ai_messages) < 2:
        return None

    # The second-most recent AI message should contain the confirmation details
    # call appointment_reader from utils.py
    appointment_reader_saver(ai_messages[1])

"""
                                Setup Session Message History
-----------------------------------------------------------------------------------------------
"""

# single-session chat history
chat_history = InMemoryChatMessageHistory()

# define a simple function to always return this single session
def get_session_history(session_id):
    return chat_history  # same in-memory chat for now

"""
                                Program's Main Execution
-----------------------------------------------------------------------------------------------
"""

generate_data_store()
db = load_rag()
# initialize the gemini model
llm = ChatGoogleGenerativeAI(
    model='gemini-2.5-flash',
    api_key = os.getenv('GEMINI_API_KEY'),
)
# initialize the retriever
retriever = db.as_retriever(search_kwargs={"k": 3})
multi_retriever = MultiQueryRetriever.from_llm(
retriever = retriever,
llm = llm,
)
# initialize runnable message history
conversation = RunnableWithMessageHistory(
    runnable = llm,
    get_session_history = get_session_history,
)

# function for api call
def executeBainiAi(user_input):
    chatbot_response = BainiAI(user_input)

    if chatbot_response is None:
        return "Maybe you want to know about our company?"

    # handle both string or AIMessage response types
    if hasattr(chatbot_response, "content"):
        content = chatbot_response.content
    elif isinstance(chatbot_response, str):
        content = chatbot_response
    else:
        try:
            content = chatbot_response.generations[0][0].text
        except Exception:
            content = "Maybe you want to know about our company?"

    # save appointment if detected
    appointment_details(content)
    return content