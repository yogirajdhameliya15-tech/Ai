from flask import Flask, render_template_string, request

app = Flask(__name__)

chat_history = []

# ---------------- HTML + CSS Template -----------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Technology Chatbot | Patel Studio</title>
<style>
    body {
        margin: 0;
        padding: 0;
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #1f1c2c, #928dab);
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .chat-container {
        background: #ffffffee;
        border-radius: 20px;
        width: 60%;
        max-width: 900px;
        box-shadow: 0 0 20px rgba(0,0,0,0.3);
        padding: 20px 30px;
        position: relative;
        overflow: hidden;
    }
    h2 {
        text-align: center;
        color: #2c3e50;
        margin-bottom: 10px;
        font-size: 28px;
    }
    .chat-box {
        height: 400px;
        overflow-y: auto;
        background: #f7f9fc;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
        border: 2px solid #ddd;
    }
    .user {
        color: #007bff;
        font-weight: 600;
        margin: 8px 0;
    }
    .bot {
        color: #28a745;
        font-weight: 600;
        margin: 8px 0;
    }
    form {
        display: flex;
        gap: 10px;
    }
    input[type="text"] {
        flex: 1;
        padding: 12px;
        border-radius: 10px;
        border: 2px solid #ccc;
        font-size: 16px;
        outline: none;
        transition: 0.3s;
    }
    input[type="text"]:focus {
        border-color: #6c63ff;
        box-shadow: 0 0 8px rgba(108, 99, 255, 0.5);
    }
    input[type="submit"] {
        background: linear-gradient(135deg, #6c63ff, #3b3b98);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 25px;
        font-weight: bold;
        font-size: 16px;
        cursor: pointer;
        transition: 0.3s;
    }
    input[type="submit"]:hover {
        transform: scale(1.05);
        background: linear-gradient(135deg, #3b3b98, #182848);
    }
    .watermark {
        text-align: center;
        margin-top: 10px;
        color: #444;
        font-size: 14px;
        font-style: italic;
        opacity: 0.8;
    }
</style>
</head>
<body>
    <div class="chat-container">
        <h2>🤖 Technology Chatbot</h2>
        <div class="chat-box" id="chatBox">
            {% for chat in history %}
                <div class="user">👤 <b>You:</b> {{ chat['user'] }}</div>
                <div class="bot">🤖 <b>Bot:</b> {{ chat['bot'] }}</div>
            {% endfor %}
        </div>
        <form method="POST">
            <input type="text" name="message" placeholder="Ask me about AI, IoT, Cloud, Cybersecurity..." required>
            <input type="submit" value="Send">
        </form>
        <div class="watermark">✨ Made by Patel Studio ✨</div>
    </div>
</body>
</html>
"""

# ---------------- Chatbot Logic -----------------
def chatbot_response(user_input):
    text = user_input.lower()

    # Greetings
    if "hello" in text or "hi" in text:
        return "Hello 👋! I'm your Technology Assistant. Ask me about AI, ML, Cloud, or Cybersecurity."

    if "how are you" in text:
        return "I'm always learning the latest in tech! 😎 How can I help you today?"

    if "bye" in text:
        return "Goodbye! 👋 Stay updated with technology!"

    # --- Technology Topics ---
    if "artificial intelligence" in text or "ai" in text:
        return ("🤖 Artificial Intelligence (AI) enables machines to think and act like humans. "
                "It includes natural language processing, robotics, and deep learning.")

    if "machine learning" in text or "ml" in text:
        return ("📊 Machine Learning teaches systems to learn from data. "
                "It includes supervised, unsupervised, and reinforcement learning.")

    if "deep learning" in text:
        return ("🧠 Deep Learning is a type of machine learning using multi-layer neural networks "
                "for tasks like image and speech recognition.")

    if "iot" in text or "internet of things" in text:
        return ("🌐 The Internet of Things (IoT) connects everyday devices to the internet — "
                "like smart homes, wearables, and industrial sensors.")

    if "cloud computing" in text or "cloud" in text:
        return ("☁️ Cloud Computing provides servers, databases, and AI services online. "
                "Providers: AWS, Azure, Google Cloud.")

    if "blockchain" in text:
        return ("⛓️ Blockchain is a decentralized ledger used in cryptocurrency and secure data sharing. "
                "It ensures transparency and immutability.")

    if "cybersecurity" in text:
        return ("🔒 Cybersecurity protects networks and data from attacks. "
                "Includes ethical hacking, encryption, and digital forensics.")

    if "robotics" in text:
        return ("🤖 Robotics combines AI, sensors, and mechanics to build intelligent machines "
                "used in manufacturing, healthcare, and defense.")

    if "ar" in text or "augmented reality" in text:
        return ("🕶️ Augmented Reality adds digital elements to the real world using smartphones or AR glasses.")

    if "vr" in text or "virtual reality" in text:
        return ("🎮 Virtual Reality immerses users in 3D simulated environments — popular in gaming and training.")

    if "data science" in text:
        return ("📈 Data Science extracts insights from large datasets using statistics, AI, and visualization tools.")

    if "big data" in text:
        return ("💾 Big Data handles huge volumes of structured and unstructured data for analytics and predictions.")

    if "quantum computing" in text:
        return ("⚛️ Quantum Computing uses qubits to perform advanced computations — much faster than classical computers.")

    if "python" in text:
        return ("🐍 Python is a simple yet powerful programming language used in AI, ML, Web Development, and Automation.")

    if "devops" in text:
        return ("🚀 DevOps integrates development and operations to enable fast software delivery and automation.")

    if "5g" in text:
        return ("📶 5G provides ultra-fast, low-latency communication — essential for IoT and smart cities.")

    if "cloud service" in text or "aws" in text:
        return ("☁️ AWS (Amazon Web Services) is a top cloud platform offering compute, database, and AI services.")

    # Fallback
    return "🤔 I'm not sure about that yet. Try asking about AI, IoT, Cloud, Cybersecurity, or any tech topic!"

# ---------------- Flask Routes -----------------
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_message = request.form["message"]
        bot_message = chatbot_response(user_message)
        chat_history.append({"user": user_message, "bot": bot_message})
    return render_template_string(HTML_TEMPLATE, history=chat_history)

if __name__ == "__main__":
    app.run(debug=True)
