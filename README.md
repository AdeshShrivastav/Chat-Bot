# Adesh's QA Bot

Adesh's QA Bot is an interactive question-answering application built with Streamlit and LangChain. It leverages Google's Generative AI (Gemini model) for intelligent responses and integrates with DuckDuckGo Search and Wikipedia for real-time information retrieval.

## Features

*   **Interactive Chat Interface**: Engage in natural language conversations.
*   **Google Gemini Integration**: Powered by Google's advanced generative AI models for comprehensive answers.
*   **Web Search Capabilities**: Utilizes DuckDuckGo Search to fetch up-to-date information.
*   **Wikipedia Integration**: Accesses Wikipedia for detailed knowledge on various topics.
*   **Chat History**: Maintains conversation context for a seamless user experience.
*   **Clear Chat Functionality**: Easily reset the conversation.

## Installation

To set up and run the bot locally, follow these steps:

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Obtain a Google API Key:**
    *   Go to the [Google AI Studio](https://aistudio.google.com/app/apikey) to generate your API key.

5.  **Set up your API Key:**
    During runtime, the Streamlit application will prompt you to enter your `GOOGLE_API_KEY` in the sidebar. Alternatively, you can set it as an environment variable:
    ```bash
    export GOOGLE_API_KEY="your_api_key_here"
    ```
    Or create a `.env` file in the project root with the following content:
    ```
    GOOGLE_API_KEY="your_api_key_here"
    ```

## Usage

To run the Streamlit application:

```bash
streamlit run bot.py
```

The application will open in your web browser. Enter your Google API Key in the sidebar, and then you can start asking questions in the chat input.

## Dependencies

The project relies on the following key libraries:

*   `langchain`
*   `langgraph`
*   `streamlit`
*   `python-dotenv`
*   `langchain-google-genai`
*   `duckduckgo-search`
*   `langchain-community`

These dependencies are listed in `requirements.txt`.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for any bugs or feature requests.

## License

This project is open-source and available under the [MIT License](LICENSE).
