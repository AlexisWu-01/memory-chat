# semantic_search.py
from sentence_transformers import SentenceTransformer, util
import torch

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_relevant_facts(query, memory, conversation_history, top_k=3):
    # Encode the query and memory
    query_embedding = model.encode(query, convert_to_tensor=True)
    memory_embeddings = model.encode(memory, convert_to_tensor=True)
    
    # Encode the conversation history
    history_text = " ".join([f"{turn['user']} {turn['assistant']}" for turn in conversation_history[-5:]])  # Consider last 5 turns
    history_embedding = model.encode(history_text, convert_to_tensor=True)
    
    # Combine query and history embeddings with more weight on the query
    combined_embedding = (0.7 * query_embedding + 0.3 * history_embedding)
    
    # Calculate cosine similarity
    cos_scores = util.cos_sim(combined_embedding, memory_embeddings)[0]
    top_results = torch.topk(cos_scores, k=top_k)
    
    relevant_facts = [memory[idx] for idx in top_results.indices]
    return relevant_facts
