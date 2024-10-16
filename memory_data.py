import random


def generate_synthetic_memory():
    # Define categories and their possible values
    categories = {
        'hobbies': ['reading', 'swimming', 'painting', 'coding', 'hiking', 'gaming', 'gardening', 'photography', 'cooking', 'dancing'],
        'foods': ['pizza', 'sushi', 'pasta', 'salad', 'steak', 'tacos', 'burgers', 'ramen', 'ice cream', 'chocolate'],
        'places': ['New York', 'Paris', 'Tokyo', 'Sydney', 'Berlin', 'Rome', 'Toronto', 'Barcelona', 'Singapore', 'Dubai'],
        'colors': ['red', 'green', 'yellow', 'purple', 'black', 'white', 'orange', 'pink', 'gray'],
        'pets': ['dog', 'cat', 'hamster', 'parrot', 'fish', 'rabbit', 'turtle', 'snake', 'lizard', 'guinea pig'],
        'sports': ['soccer', 'basketball', 'tennis', 'baseball', 'running', 'cycling', 'skiing', 'surfing', 'boxing', 'volleyball'],
        'music_genres': ['rock', 'jazz', 'classical', 'pop', 'hip-hop', 'electronic', 'country', 'blues', 'reggae', 'metal'],
        'movies': ['Inception', 'The Godfather', 'The Matrix', 'Interstellar', 'Parasite', 'The Dark Knight', 'Pulp Fiction', 'Forrest Gump', 'Fight Club', 'The Shawshank Redemption'],
        'books': ['1984', 'To Kill a Mockingbird', 'The Great Gatsby', 'Moby Dick', 'War and Peace', 'Pride and Prejudice', 'The Catcher in the Rye', 'The Hobbit', 'Jane Eyre', 'Brave New World'],
        'professions': ['doctor', 'teacher', 'artist', 'writer', 'musician', 'scientist', 'architect', 'lawyer', 'designer']
    }

    # Define mandatory facts with categories
    mandatory_facts = [
        {"category": "colors", "fact": "The user's favorite color is blue."},
        {"category": "allergies", "fact": "The user is allergic to peanuts."},
        {"category": "transportation", "fact": "The user's preferred mode of transportation is cycling."},
        {"category": "pets", "fact": "The user has a pet cat named Jojo."},
        {"category": "professions", "fact": "The user currently works as a software engineer."}
    ]

    # Define optional facts templates with categories
    fact_templates = [
        ("hobbies", lambda: f"The user loves {random.choice(categories['hobbies'])}."),
        ("foods", lambda: f"The user enjoys eating {random.choice(categories['foods'])}."),
        ("places", lambda: f"The user wants to visit {random.choice(categories['places'])}."),
        ("colors", lambda: f"The user's likes color {random.choice(categories['colors'])}."),
        ("pets", lambda: f"The user owns a {random.choice(categories['pets'])}."),
        ("sports", lambda: f"The user plays {random.choice(categories['sports'])} regularly."),
        ("music_genres", lambda: f"The user listens to {random.choice(categories['music_genres'])} music."),
        ("movies", lambda: f"The user like movies like {random.choice(categories['movies'])}."),
        ("books", lambda: f"The user is currently reading {random.choice(categories['books'])}."),
        ("professions", lambda: f"The user worked as a {random.choice(categories['professions'])}.")
    ]

    # Initialize memory with mandatory facts
    memory = [fact["fact"] for fact in mandatory_facts]

    # Generate remaining facts
    num_optional_facts = 100 - len(mandatory_facts)
    for _ in range(num_optional_facts):
        category, template = random.choice(fact_templates)
        fact = template()
        # Avoid duplicate facts
        if fact not in memory:
            memory.append(fact)

    # Shuffle the memory to mix mandatory and optional facts
    random.shuffle(memory)
    return memory

user_memory = generate_synthetic_memory()

conversation_history = []

def update_conversation_history(user_input, assistant_response, memory_used, new_facts, max_history=10):
    global conversation_history
    conversation_history.append({
        'user': user_input,
        'assistant': assistant_response,
        'memory': memory_used,
        'new_facts': new_facts
    })

    # Maintain a limited conversation history
    if len(conversation_history) > max_history:
        conversation_history = conversation_history[-max_history:]
