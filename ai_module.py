import openai
import os

# Safely initialize OpenAI client
try:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        client = openai.OpenAI(api_key=api_key)
    else:
        client = None
except Exception as e:
    print(f"OpenAI initialization error: {e}")
    client = None

# Basic fallback AI responses
def get_fallback_response(command):
    command = command.lower()
    if "einstein" in command:
        return "Albert Einstein was a theoretical physicist famous for the theory of relativity."
    elif "newton" in command:
        return "Isaac Newton formulated the laws of motion and gravity."
    elif "tesla" in command:
        return "Nikola Tesla contributed to the design of modern AC electricity."
    elif "python" in command:
        return "Python is a high-level programming language known for its simplicity."
    elif "how are you" in command:
        return "I'm functioning well, thank you!"
    elif "what can you do" in command:
        return "I can tell time, play music, open websites, and answer your questions."
    else:
        return "I'm in offline mode. I can still help with basic tasks."

# Process user input using OpenAI or fallback
def aiProcess(command):
    command_lower = command.lower()
    
    # Fallback trigger keywords
    fallback_keywords = ["einstein", "newton", "tesla"]

    # If any keyword is found in the query, force fallback
    if any(keyword in command_lower for keyword in fallback_keywords):
        return get_fallback_response(command)

    if client:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Jarvis, a helpful AI assistant."},
                    {"role": "user", "content": command},
                ],
                temperature=0.6,
                max_tokens=100,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI error: {e}")
    
    return get_fallback_response(command)
