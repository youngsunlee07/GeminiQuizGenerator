# Quiz Builder Application

This project is a web application that generates quiz questions from PDF documents. It uses Streamlit for document upload, Google Vertex AI for question generation, and ChromaDB for document management.

## Components
1. **DocumentProcessor**: Uploads and processes PDF documents.
2. **EmbeddingClient**: Creates embeddings of the documents using Google Vertex AI.
3. **ChromaCollectionCreator**: Stores and retrieves documents using ChromaDB.
4. **QuizGenerator**: Generates quiz questions based on the topic and documents.
5. **QuizManager**: Manages and displays the generated quiz questions.

## Installation and Execution
1. Create a new project on Google Cloud Platform:
    - Enable the Vertex AI API.
    - Create a service account:
        - Assign a name and role to the account.
    - Generate a key:
        - Choose JSON format as the key type, which is required for SDK authentication.

2. Clone this repository:
    ```bash
    git clone https://github.com/youngsunlee07/GeminiQuizify.git
    ```

3. Navigate to the project directory:
    ```bash
    cd GoogleGemini
    ```

4. Install the required packages:
    ```bash
    pip install streamlit google-cloud-aiplatform
    ```

5. Install and initialize the Google Cloud SDK:
    - Follow the [official installation guide](https://cloud.google.com/sdk/docs/install) to install the Google Cloud SDK.
    - After installation, initialize the SDK using the following command:
      ```bash
      gcloud init
      ```
    - Authenticate and set up your project with the gcloud CLI:
      ```bash
      gcloud auth application-default login
      ```

6. Set the Google Application Credentials:
    ```bash
    export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    ```

7. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

8. Run the Streamlit application:
    ```bash
    streamlit run app.py
    ```

## Usage
1. Run the `task_10.py` application and upload a PDF file.
2. Enter the quiz topic and the number of questions.
3. Click the `Submit` button to store the document in ChromaDB and generate quiz questions.
4. Review the generated quiz questions and navigate through them using the `Next` and `Previous` buttons.

## Key Features
- PDF document upload and processing.
- Document embedding generation using Google Vertex AI.
- Document storage and retrieval using ChromaDB.
- Quiz question generation based on topics.
- Quiz question management and navigation.

## Contact

If you have any questions or suggestions about the project, please contact me at youngsun.lee07@gmail.com.
