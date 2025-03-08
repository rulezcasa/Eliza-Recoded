from flask import Flask, render_template, request, jsonify
import re
import random
from flask_cors import CORS  
import os

app = Flask(__name__)
CORS(app)  

class Eliza:
    def __init__(self):
        self.reflections = {
            "i am": "you are",
            "i was": "you were",
            "i": "you",
            "i'm": "you are",
            "my": "your",
            "me": "you",
            "am": "are"
        }
        
        self.patterns = [
            (r"i need (.*)", ["Why do you need \1?", "Would it really help you to get \1?", "Are you sure you need \1?"]),
            (r"why don'?t you (.*)", ["Do you really think I don't \1?", "Perhaps eventually I will \1.", "Do you want me to \1?"]),
            (r"why can'?t i (.*)", ["Do you think you should be able to \1?", "If you could \1, what would you do?", "I don't know -- why can't you \1?", "Have you really tried?"]),
            (r"i can'?t (.*)", ["How do you know you can't \1?", "Perhaps you could \1 if you tried.", "What would it take for you to \1?"]),
            (r"i am (.*)", ["Did you come to me because you are \1?", "How long have you been \1?", "How do you feel about being \1?"]),
            (r"are you (.*)", ["Why does it matter whether I am \1?", "Would you prefer if I were not \1?", "Perhaps you believe I am \1.", "I may be \1 -- what do you think?"]),
            (r"what (.*)", ["Why do you ask?", "How would an answer to that help you?", "What do you think?"]),
            (r"how (.*)", ["How do you suppose?", "Perhaps you can answer your own question.", "What is it you're really asking?"]),
            (r"because (.*)", ["Is that the real reason?", "What other reasons come to mind?", "Does that reason apply to anything else?", "If \1, what else must be true?"]),
            (r"(.*) sorry (.*)", ["There are many times when no apology is needed.", "What feelings do you have when you apologize?"]),
            (r"hello(.*)", ["Hello... I'm glad you could drop by today.", "Hi there... how are you today?", "Hello, how are you feeling today?"]),
            (r"i think (.*)", ["Do you doubt \1?", "Do you really think so?", "But you're not sure \1?"]),
            (r"(.*) friend (.*)", ["Tell me more about your friends.", "Why don't you tell me about a childhood friend?", "What do you value most in a friend?"]),
            (r"yes", ["You seem quite sure.", "OK, but can you elaborate a bit?"]),
            (r"(.*) computer(.*)", ["Are you really talking about me?", "Does it seem strange to talk to a computer?", "How do computers make you feel?", "Do you feel threatened by computers?"]),
            (r"is it (.*)", ["Do you think it is \1?", "Perhaps it's \1 -- what do you think?", "If it were \1, what would you do?", "It could well be that \1."]),
            (r"my family (.*)", ["Family relationships can be complicated. What about your family bothers you?", "Tell me more about your family.", "How do you usually deal with family issues?"]),
            (r"(.*)", ["Please tell me more.", "Let's change focus a bit... Tell me about your family.", "Can you elaborate on that?", "Why do you say that \1?", "go on, I'm listening"])
        ]

    def reflect(self, text):
        words = text.lower().split()
        transformed_words = [self.reflections.get(word, word) for word in words]
        return " ".join(transformed_words)
    
    def respond(self, text):
        for pattern, responses in self.patterns:
            match = re.match(pattern, text.lower())
            if match:
                response = random.choice(responses)
                return response.replace("\1", self.reflect(match.group(1)))
        return "I see. Please go on."

eliza = Eliza()

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    response = eliza.respond(user_input)
    return jsonify({"response": response})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port, debug=True)

