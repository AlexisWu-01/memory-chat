# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
from openai import OpenAI
from memory_data import user_memory, update_memory, conversation_history, update_conversation_history
from semantic_search import get_relevant_facts

app = Flask(__name__)

# Set your OpenAI API key
from api_key import openai_api_key

client = OpenAI(api_key=openai_api_key)

@app.route('/', methods=['GET', 'POST'])
def chat():
    global user_memory, conversation_history
    if request.method == 'POST':
        user_input = request.form['user_input']
        # Retrieve relevant facts considering conversation history
        relevant_facts = get_relevant_facts(user_input, user_memory, conversation_history)
        
        # Prepare the messages for the LLM, including conversation history
        messages = [
            {"role": "system", "content": "You are a helpful assistant with access to user memory. Use the relevant facts provided to personalize your responses."}
        ]
        
        # Add conversation history
        for turn in conversation_history:
            messages.append({"role": "user", "content": turn['user']})
            messages.append({"role": "assistant", "content": turn['assistant']})
        
        # Add current user input and relevant facts
        messages.append({"role": "user", "content": f"Relevant Facts: {relevant_facts}\n\nUser Input: {user_input}"})
        
        # Get response from LLM
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150
        )
        assistant_response = response.choices[0].message.content.strip()
        
        # Update memory based on the conversation
        user_memory = update_memory(user_input, assistant_response, user_memory)
        
        # Update conversation history
        update_conversation_history(user_input, assistant_response, relevant_facts)
        
        return jsonify({
            'response': assistant_response,
            'memory': relevant_facts
        })

    return render_template('chat.html', conversation=conversation_history)

@app.route('/memory', methods=['GET', 'POST'])
def memory():
    global user_memory
    if request.method == 'POST':
        # Handle memory edits
        new_memory = request.form.getlist('memory')
        user_memory = new_memory
        return redirect(url_for('memory'))
    return render_template('memory.html', memory=user_memory)

if __name__ == '__main__':
    app.run(debug=True)
