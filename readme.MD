# Chat with Memory Web Application

This web application allows users to engage in a conversation with an AI assistant that has access to user memory. The assistant can personalize responses based on the user's history and preferences.

## Features

1. **Chat Interface**: Engage in real-time conversations with the AI assistant.
2. **Memory System**: The application maintains a memory of user information and preferences.
3. **Semantic Search**: Utilizes semantic search to retrieve relevant facts from memory for each conversation turn.
4. **Editable Memory**: Users can view and edit their memory directly through the interface.
5. **Conversation History**: The application keeps track of recent conversation turns for context.

## How to Use

### Setting Up

1. Clone the repository to your local machine.
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up your OpenAI API key in the `api_key.py` file.

### Running the Application

1. Start the Flask server:
   ```
   python app.py
   ```
2. Open your web browser and navigate to `http://localhost:5000`.

### Using the Chat Interface

1. The main page displays the chat interface.
2. Type your message in the input box at the bottom of the page.
3. Press "Send" or hit Enter to send your message.
4. The AI assistant will respond, taking into account your message and relevant information from your memory.
5. The conversation history and used memory facts are displayed in the chat window.

### Viewing and Editing Memory

1. Click on the "View/Edit Memory" link at the bottom of the chat page.
2. You'll be taken to a page where you can view all the facts in your memory.
3. Edit the text in the textarea to modify your memory.
4. Click "Save Memory" to update your memory with the changes.

## Key Components

- **Chat Template**: The main chat interface is defined in `templates/chat.html`.
- **Memory Template**: The memory editing interface is defined in `templates/memory.html`.
- **Flask Application**: The main application logic is in `app.py`.
- **Memory Management**: User memory and conversation history are managed in `memory_data.py`.
- **Semantic Search**: Relevant fact retrieval is handled by `semantic_search.py`.

## Notes

- The application uses GPT-3.5-turbo for generating responses.
- The memory system starts with a set of synthetic facts that can be customized or replaced with real user data.
- The semantic search functionality uses the 'all-MiniLM-L6-v2' model for embedding generation.

Enjoy chatting with your personalized AI assistant!

