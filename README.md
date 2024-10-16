# Chat with Memory Web Application

This web application allows users to engage in a conversation with an AI assistant that has access to user memory. The assistant can personalize responses based on the user's history and preferences.

## Features

1. **Interactive Chat Interface**: Engage in real-time conversations with the AI assistant through a user-friendly chat box.
2. **Memory System**: The application maintains a memory of user information and preferences.
3. **Semantic Search**: Utilizes semantic search to retrieve relevant facts from memory for each conversation turn.
4. **Editable Memory**: Users can view and edit their memory directly through the interface.
5. **Conversation History**: The application keeps track of recent conversation turns for context.

## Demo

![Chat with Memory Demo](https://github.com/AlexisWu-01/memory-chat/blob/main/demo/Screenshot.png)

To see a short video to see this in action: https://github.com/user-attachments/assets/2a4de4ce-d73e-4903-a114-dfeae129b4c1
https://youtu.be/xJviodVrxZk


*Screenshot: An example conversation with the AI assistant, showcasing the chat interface and memory usage.*

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

1. The main page displays the chat interface with a message input box at the bottom.
2. Type your message in the input box and press "Send" or hit Enter to send your message.
3. The AI assistant will respond, taking into account your message and relevant information from your memory.
4. The conversation history, used memory facts, and newly learned facts are displayed in the chat window.
5. To view or edit your memory, click on the "View/Edit Memory" link at the bottom of the chat page.

## Key Components

- **Chat Interface**: The main chat interface is defined in `templates/chat.html`.
- **Memory Interface**: The memory editing interface is defined in `templates/memory.html`.
- **Flask Application**: The main application logic is in `app.py`.
- **Memory Management**: User memory and conversation history are managed in `memory_data.py`.
- **Semantic Search**: Relevant fact retrieval is handled by `semantic_search.py`.

## Notes

- The application uses GPT-3.5-turbo for generating responses.
- The memory system starts with a set of synthetic facts that can be customized or replaced with real user data.
- The semantic search functionality uses the 'all-MiniLM-L6-v2' model for embedding generation.

Enjoy chatting with your personalized AI assistant!
