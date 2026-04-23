import ollama

def get_ai_response(prompt):
    response = ollama.chat(
        model="llama3:8b",   # USE INSTALLED MODEL
        messages=[{"role": "user", "content": prompt}],
        options={
            "num_predict": 500,   # FAST (IMPORTANT)
            "temperature": 0.3
        }
    )
    return response["message"]["content"]


