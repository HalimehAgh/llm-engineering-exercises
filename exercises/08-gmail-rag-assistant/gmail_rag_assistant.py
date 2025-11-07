from email.mime import message
import os
import gradio as gr
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import base64
from datetime import datetime
import openai
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory



# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class GmailRAGAssistant:
    def __init__(self):
        self.service = None
        self.vectorstore = None
        self.qa_chain = None
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )

    def authenticate_gmail(self):
        """Authenticate with Gmail API"""
        creds = None

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('gmail', 'v1', credentials=creds)
        return "✅ Gmail authentication successful!"

    def fetch_emails(self, max_results=100):
        """Fetch emails from Gmail"""
        if not self.service:
            return "❌ Please authenticate first!"

        try:
            results = self.service.users().messages().list(
                userId='me',
                maxResults=max_results
            ).execute()

            messages = results.get('messages', [])
            if not messages:
                return "No messages found."

            emails = []
            for msg in messages:
                message = self.service.users().messages().get(
                    userId='me',
                    id=msg['id'],
                    format='full'
                ).execute()

                email_data = self.parse_email(message)
                emails.append(email_data)

            return emails

        except Exception as e:
            return f"❌ Error fetching emails: {str(e)}"

    def parse_email(self, message):
        """Parse email message"""
        headers = message['payload']['headers']

        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
        date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')

        body = ""
        if 'parts' in message['payload']:
            for part in message['payload']['parts']:
                if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    break
        elif 'body' in message['payload'] and 'data' in message['payload']['body']:
            body = base64.urlsafe_b64decode(message['payload']['body']['data']).decode('utf-8')

        return {'subject': subject, 'sender': sender, 'date': date, 'body': body}

 

    def create_vector_store(self, emails):
        """Create vector store from emails"""
        if isinstance(emails, str):
            return emails

        documents = [
            Document(
                page_content=f"Subject: {email['subject']}\nFrom: {email['sender']}\nDate: {email['date']}\n\n{email['body']}",
                metadata=email
            )
            for email in emails
        ]

        # Use smaller chunks to stay within token limits
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        splits = splitter.split_documents(documents)

        embeddings = OpenAIEmbeddings(chunk_size=100)  # Process 100 chunks at a time

        # Create FAISS index with batched embeddings
        self.vectorstore = FAISS.from_documents(
            documents=splits,
            embedding=embeddings
        )
        
        # Save to disk
        self.vectorstore.save_local("faiss_index")

        return f"✅ Vector store created with {len(splits)} chunks from {len(emails)} emails!"



    def setup_qa_chain(self):
        """Setup RAG QA chain"""
        if not self.vectorstore:
            return "❌ Please create vector store first!"

        from langchain.prompts import PromptTemplate
        
        # Create a more flexible prompt
        prompt_template = """You are a helpful assistant that answers questions about the user's emails.

    Use the following email context to answer questions when relevant:
    {context}

    Guidelines:
    - For greetings or general conversation, respond naturally and warmly
    - For questions about emails, use the context provided
    - If the context doesn't contain relevant information to answer an email question, say "I don't have any emails about that topic"
    - Always respond in English
    - Be friendly and conversational

    Question: {question}

    Answer:"""
        
        PROMPT = PromptTemplate(
            template=prompt_template, 
            input_variables=["context", "question"]
        )

        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3  # Slightly higher for more natural conversation
        )

        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 100}), 
            memory=self.memory,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": PROMPT},
            verbose=False
        )

        return "✅ QA chain ready!"

    def answer_question(self, question):
        """Answer a question using RAG"""
        if not self.qa_chain:
            return "❌ Please setup the system first!"

        try:
            result = self.qa_chain.invoke({"question": question})
            answer = result['answer']

            # Check if this is a greeting or general chat (not an email question)
            greeting_words = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "thanks", "thank you"]
            is_greeting = any(word in question.lower() for word in greeting_words)
            
            # Check if answer indicates no information found
            no_info_phrases = ["i don't have", "i don't know", "no sé", "ich weiß nicht", "cannot find", "no emails"]
            has_no_info = any(phrase in answer.lower() for phrase in no_info_phrases)

            # Only add sources if it's not a greeting and has relevant info
            if not is_greeting and not has_no_info and answer:
                sources = []
                for doc in result['source_documents']:
                    sources.append(f"📧 {doc.metadata.get('subject', 'N/A')} (from {doc.metadata.get('sender', 'N/A')})")

                if sources:
                    unique_sources = list(set(sources[:3]))
                    answer += "\n\n**Sources:**\n" + "\n".join(unique_sources)

            return answer

        except Exception as e:
            return f"❌ Error: {str(e)}"


# === Gradio Interface ===

assistant = GmailRAGAssistant()


def authenticate():
    return assistant.authenticate_gmail()


def load_emails(num_emails):
    status_msgs = ["Fetching emails..."]
    emails = assistant.fetch_emails(max_results=int(num_emails))

    if isinstance(emails, str):
        return emails

    status_msgs.append(f"✅ Fetched {len(emails)} emails")
    status_msgs.append("Creating vector store...")
    result = assistant.create_vector_store(emails)
    status_msgs.append(result)

    status_msgs.append("Setting up QA chain...")
    result = assistant.setup_qa_chain()
    status_msgs.append(result)

    return "\n".join(status_msgs)


def chat(message, history):
    """Chat interface function"""
    if history is None:
        history = []
    
    response = assistant.answer_question(message)
    
    # Append message and response to history in the correct format
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": response})
    
    return history


with gr.Blocks(title="Gmail RAG Assistant", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 📧 Gmail RAG Assistant\nAsk questions about your emails using RAG.")
    with gr.Tab("Setup"):
        auth_btn = gr.Button("🔐 Authenticate Gmail", variant="primary")
        auth_output = gr.Textbox(label="Status", lines=1)
        num_emails = gr.Slider(minimum=10, maximum=500, value=100, step=10, label="Number of emails")
        load_btn = gr.Button("📥 Load Emails", variant="primary")
        load_output = gr.Textbox(label="Status", lines=10)

    with gr.Tab("Chat"):
        chatbot = gr.Chatbot(height=400, type="messages")
        msg = gr.Textbox(label="Your Question", placeholder="e.g., What emails mention the project deadline?", lines=2)
        with gr.Row():
            submit = gr.Button("Send", variant="primary")
            clear = gr.Button("Clear")

    auth_btn.click(authenticate, outputs=auth_output)
    load_btn.click(load_emails, inputs=num_emails, outputs=load_output)
    def submit_message(message, history):
        return chat(message, history), ""  # Return updated history and clear input

    submit.click(submit_message, inputs=[msg, chatbot], outputs=[chatbot, msg])
    msg.submit(submit_message, inputs=[msg, chatbot], outputs=[chatbot, msg])
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch(share=False, server_name="127.0.0.1", server_port=7860)
