# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
from openai import OpenAI
from memory_data import user_memory, conversation_history, update_conversation_history
import json
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Set your OpenAI API key
from api_key import openai_api_key

client = OpenAI(api_key=openai_api_key)
@app.route('/', methods=['GET', 'POST'])
def chat():
    global user_memory, conversation_history

    try:
        if request.method == 'POST':
            user_input = request.form.get('user_input', '').strip()

            # Handle case where no input was provided
            if not user_input:
                logging.warning("Empty user input received.")
                return jsonify({"error": "User input is required."}), 400

            # Prepare the context with memory and conversation history
            context = (
                f"User Query: {user_input}\n\n"
                f"User Memory:\n{chr(10).join(user_memory)}\n\n"
                f"Conversation History:\n{format_conversation_history(conversation_history)}"
            )

        # Refined prompt with concise instructions and clear examples
            prompt = """
            You are a helpful assistant that utilizes user memory and conversation history to provide accurate and personalized responses.

            **Tasks:**
            1. **Select up to 5 relevant facts** from the user memory that are **most contextually related** to the user's query.
            - Use recent conversation context and the specific content of the query to determine relevance.
            - **Only include facts essential to the query** or **necessary** to enhance the response meaningfully.
            - Avoid including unrelated or tangential information, even if it is known about the user.
            2. **Craft a concise, personalized response** based on the user's query along with relevant facts and recent conversation.
            - Directly address the user's query while integrating relevant details from memory where helpful.
            3. **Extract any new factual information** from the user's query only to update the memory.
            - Ensure only new, relevant facts are added, avoiding redundancies or irrelevant details.
            4. **Respond strictly in JSON format only, with no additional comments or explanations.**

            **Respond in the following JSON format:**
            {
                "memory_used": ["..."],
                "assistant_response": "...",
                "new_facts": ["..."]
            }

            ---
            **Example 1:**
            User Query: What is my favorite color?
            User Memory:
            - The user's favorite color is blue.
            - The user enjoys eating tacos.
            - The user likes movies like Parasite.
            - The user plays basketball regularly.
            - The user's preferred mode of transportation is cycling.
            Conversation History:
            User: What is my favorite color?
            Assistant: Based on your memory, your favorite color is blue.

            Response:
            {
                "memory_used": ["The user's favorite color is blue.", "The user likes color red."],
                "assistant_response": "Your favorite color is blue.",
                "new_facts": []
            }
            ---
            **Example 2:**
            User Query: I just got a new puppy named Max.
            User Memory:
            - The user has a pet cat named Jojo.
            - The user enjoys activities related to water like swimming.
            - The user plays basketball regularly.
            - The user likes movies like Inception.
            Conversation History:
            User: I just got a new puppy named Max.
            Assistant: That's exciting! Now you have a pet cat named Jojo and a new puppy named Max.

            Response:
            {
                "memory_used": ["The user has a pet cat named Jojo."],
                "assistant_response": "Congratulations on your new puppy, Max! Now you have a pet cat named Jojo and a new puppy.",
                "new_facts": ["The user got a new puppy named Max."]
            }
            ---
            **Example 3:**
            User Query: What were we just talking about?
            User Memory:
            - The user has a pet cat named Jojo.
            - The user got a new puppy named Max.
            - The user enjoys eating tacos.
            - The user likes movies like Inception.
            - The user currently works as a software engineer.
            Conversation History:
            User: I just got a new puppy named Max.
            Assistant: Congratulations on your new puppy, Max! Now you have a pet cat named Jojo and a new puppy.
            User: What were we just talking about?

            Response:
            {
                "memory_used": [
                    "The user has a pet cat named Jojo.",
                    "The user got a new puppy named Max."
                ],
                "assistant_response": "We were discussing your pets. You have a pet cat named Jojo and a new puppy named Max.",
                "new_facts": []
            }
            ---
            **Example 4 (No New Facts):**
            User Query: Do I like sushi?
            User Memory:
            - The user is allergic to peanuts.
            - The user enjoys eating tacos.
            - The user likes movies like Inception.
            - The user currently works as a software engineer.
            Conversation History:
            User: Do I like sushi?
            Assistant: Based on your memory, there's no information about your preference for sushi.

            Response:
            {
                "memory_used": [],
                "assistant_response": "There's no information about your preference for sushi in your memory.",
                "new_facts": []
            }
            ---
            **Context for this interaction:**
            {context}

            """


            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": context}
                    ],
                    max_tokens=500,
                    temperature=0.3
                )
            except Exception as e:
                logging.exception("OpenAI API call failed.")
                return jsonify({"error": "Failed to communicate with OpenAI API."}), 500

        # Parse the response from OpenAI
            output = response.choices[0].message.content.strip()
            logging.debug(f"API Response: {output}")

            # Remove ```json and ``` from the output
            output = output.replace("```json", "").replace("```", "").strip()
            try:
                result = json.loads(output)
                memory_used = result.get("memory_used", [])
                assistant_response = result.get("assistant_response", "")
                new_facts = result.get("new_facts", [])
            except json.JSONDecodeError:
                logging.exception("JSON decoding failed.")
                return jsonify({"error": "Invalid response format from OpenAI API."}), 500

            # Update memory if new facts are found
            if new_facts:
                user_memory.extend(new_facts)
                # Preserve order and ensure uniqueness
                user_memory = list(dict.fromkeys(user_memory))[-100:]  # Keep only unique facts, limit to 100

            # Update conversation history
            update_conversation_history(user_input, assistant_response, memory_used, new_facts)
            # Return the response as JSON
            return jsonify({
                'response': assistant_response,
                'memory': memory_used,
                'new_facts': new_facts
            })

        # Render the chat page for GET requests
        return render_template('chat.html', conversation=conversation_history)

    except Exception as e:
        logging.exception("An unexpected error occurred.")
        return jsonify({"error": "An internal error occurred."}), 500

# Memory management route
@app.route('/memory', methods=['GET', 'POST'])
def memory():
    global user_memory
    if request.method == 'POST':
        new_memory = request.form.getlist('memory')
        user_memory = new_memory
        return redirect(url_for('memory'))
    return render_template('memory.html', memory=user_memory)

def format_conversation_history(history):
    """Format the conversation history for context in the prompt."""
    return "\n".join(
        f"User: {item['user']}\nAssistant: {item['assistant']}\n" for item in history
    )

if __name__ == '__main__':
    app.run(debug=True)
