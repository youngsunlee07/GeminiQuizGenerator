import sys
import os
import streamlit as st
sys.path.append(os.path.abspath('../../'))
from tasks.task_3.task_3 import DocumentProcessor
from tasks.task_4.task_4 import EmbeddingClient
from tasks.task_5.task_5 import ChromaCollectionCreator

if __name__ == "__main__":
    st.header("Quizzify")

    # Configuration for EmbeddingClient
    embed_config = {
        "model_name": "textembedding-gecko@003",
        "project": "geminiquizify-425218",
        "location": "us-central1"
    }
    
    screen = st.empty() # Screen 1, ingest documents
    with screen.container():
        processor = DocumentProcessor() # Initialize from Task 3
        processor.ingest_documents()
    
        embed_config = {
            "model_name": "textembedding-gecko@003",
            "project": "geminiquizify-425218",
            "location": "us-central1"
        }
    
        embed_client = EmbeddingClient(**embed_config) # Initialize from Task 4
    
        chroma_creator = ChromaCollectionCreator(processor, embed_client)

        with st.form("Load Data to Chroma"):
            st.subheader("Quiz Builder")
            st.write("Select PDFs for Ingestion, the topic for the quiz, and click Generate!")
            
            topic_input = st.text_input("Topic for Generative Quiz")
            num_questions = st.slider("Number of Questions", min_value=1, max_value=10) 
            
            document = None
            
            submitted = st.form_submit_button("Submit")
            if submitted:
                chroma_creator.create_chroma_collection()
                st.success("Chroma collection created successfully!")
                document = chroma_creator.query_chroma_collection(topic_input)
                
    if document:
        screen.empty() # Screen 2
        with st.container():
            st.header("Query Chroma for Topic, top Document: ")
            st.write(document)