import streamlit as st
import os
import sys
import json
sys.path.append(os.path.abspath('../../'))
from tasks.task_3.task_3 import DocumentProcessor
from tasks.task_4.task_4 import EmbeddingClient
from tasks.task_5.task_5 import ChromaCollectionCreator

from langchain_core.prompts import PromptTemplate
from langchain_google_vertexai import VertexAI

class QuizGenerator:
    def __init__(self, topic=None, num_questions=1, vectorstore=None):
        if not topic:
            self.topic = "General Knowledge"
        else:
            self.topic = topic

        if num_questions > 10:
            raise ValueError("Number of questions cannot exceed 10.")
        self.num_questions = num_questions

        self.vectorstore = vectorstore
        self.llm = None
        self.question_bank = [] # Initialize the question bank to store questions
        self.system_template = """
            You are a subject matter expert on the topic: {topic}
            
            Follow the instructions to create a quiz question:
            1. Generate a question based on the topic provided and context as key "question"
            2. Provide 4 multiple choice answers to the question as a list of key-value pairs "choices"
            3. Provide the correct answer for the question from the list of answers as key "answer"
            4. Provide an explanation as to why the answer is correct as key "explanation"
            
            You must respond as following structure, Don't make it in JSON markdown format:
            {{
                "question": "<question>",
                "choices": [
                    {{"key": "A", "value": "<choice>"}},
                    {{"key": "B", "value": "<choice>"}},
                    {{"key": "C", "value": "<choice>"}},
                    {{"key": "D", "value": "<choice>"}}
                ],
                "answer": "<answer key from choices list>",
                "explanation": "<explanation as to why the answer is correct>"
            }}
            
            Context: {context}
            """
    
    def init_llm(self):
        self.llm = VertexAI(
            model_name = "gemini-pro",
            temperature = 0.8, # Increased for less deterministic questions 
            max_output_tokens = 500
        )

    def generate_question_with_vectorstore(self):
        if not self.llm:
            self.init_llm()
        if not self.vectorstore:
            raise ValueError("Vectorstore not provided.")
        
        from langchain_core.runnables import RunnablePassthrough, RunnableParallel

        # Enable a Retriever
        retriever = self.vectorstore.as_retriever()
        
        # Use the system template to create a PromptTemplate
        prompt = PromptTemplate.from_template(self.system_template)
        
        # RunnableParallel allows Retriever to get relevant documents
        # RunnablePassthrough allows chain.invoke to send self.topic to LLM
        setup_and_retrieval = RunnableParallel(
            {"context": retriever, "topic": RunnablePassthrough()}
        )
        # Create a chain with the Retriever, PromptTemplate, and LLM
        chain = setup_and_retrieval | prompt | self.llm 

        # Invoke the chain with the topic as input
        response = chain.invoke(self.topic)
        return response

    def generate_quiz(self) -> list:
        self.question_bank = [] # Reset the question bank
        
        for _ in range(self.num_questions): 
            question_str = self.generate_question_with_vectorstore() 
            
            try:
                question = json.loads(question_str)
            except json.JSONDecodeError:
                print("Failed to decode question JSON.")
                continue  # Skip this iteration if JSON decoding fails

            # Validate the question using the validate_question method
            if self.validate_question(question):
                print("Successfully generated unique question")
                self.question_bank.append(question)
            else:
                print("Duplicate or invalid question detected.")
                
        return self.question_bank

    def validate_question(self, question: dict) -> bool:
        for q in self.question_bank:
            if q['question'] == question['question']:
                return False
    
        is_unique = True
        return is_unique


# Test Generating the Quiz
if __name__ == "__main__":
    
    embed_config = {
        "model_name": "textembedding-gecko@003",
        "project": "geminiquizify-425218",
        "location": "us-central1"
    }
    
    screen = st.empty()
    with screen.container():
        st.header("Quiz Builder")
        processor = DocumentProcessor()
        processor.ingest_documents()
    
        embed_client = EmbeddingClient(**embed_config) # Initialize from Task 4
    
        chroma_creator = ChromaCollectionCreator(processor, embed_client)
    
        question = None
        question_bank = None
    
        with st.form("Load Data to Chroma"):
            st.subheader("Quiz Builder")
            st.write("Select PDFs for Ingestion, the topic for the quiz, and click Generate!")
            
            topic_input = st.text_input("Topic for Generative Quiz", placeholder="Enter the topic of the document")
            questions = st.slider("Number of Questions", min_value=1, max_value=10, value=1)
            
            submitted = st.form_submit_button("Submit")
            if submitted:
                chroma_creator.create_chroma_collection()
                
                st.write(topic_input)
                
                # Test the Quiz Generator
                generator = QuizGenerator(topic_input, questions, chroma_creator)
                question_bank = generator.generate_quiz()
                question = question_bank[0]

    if question_bank:
        screen.empty()
        with st.container():
            st.header("Generated Quiz Question: ")
            for question in question_bank:
                st.write(question)