from flask import Flask, render_template_string, request, redirect, url_for, session
import agents

app = Flask(__name__)
app.secret_key = 'OPENAI_API_KEY'  # Geliştirirken değiştirin

HTML = '''
<!doctype html>
<html lang="tr">
<head>
    <meta charset="utf-8">
    <title>OpenAI Sohbet Botu</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Roboto', Arial, sans-serif;
            background: #181c24;
            margin: 0;
            min-height: 100vh;
        }
        .container {
            max-width: 480px;
            margin: 40px auto;
            background: #23283a;
            padding: 0 0 16px 0;
            border-radius: 16px;
            box-shadow: 0 4px 24px #0005;
            overflow: hidden;
        }
        .header {
            background: #1a1e2d;
            padding: 24px 0 16px 0;
            text-align: center;
            color: #fff;
            border-bottom: 1px solid #2c3147;
        }
        .header .icon {
            font-size: 2.5rem;
            margin-bottom: 8px;
            display: block;
        }
        .header h2 {
            margin: 0;
            font-size: 2rem;
            font-weight: 700;
            letter-spacing: 1px;
        }
        .history {
            max-height: 400px;
            overflow-y: auto;
            padding: 24px 16px 8px 16px;
            background: #23283a;
        }
        .msg-bubble {
            display: inline-block;
            padding: 12px 16px;
            border-radius: 18px;
            margin-bottom: 10px;
            max-width: 80%;
            word-break: break-word;
            font-size: 1.08rem;
            box-shadow: 0 2px 8px #0002;
        }
        .msg-user {
            background: linear-gradient(90deg, #3a8dde 60%, #5ec6fa 100%);
            color: #fff;
            align-self: flex-end;
            margin-left: 20%;
        }
        .msg-assistant {
            background: linear-gradient(90deg, #2c3147 60%, #4e5370 100%);
            color: #e0e6f7;
            align-self: flex-start;
            margin-right: 20%;
        }
        .msg-system {
            color: #b0b6c6;
            font-style: italic;
            text-align: center;
            margin-bottom: 10px;
        }
        form {
            display: flex;
            gap: 8px;
            padding: 0 16px;
            margin-top: 8px;
        }
        input[type=text] {
            flex: 1;
            padding: 12px;
            border-radius: 8px;
            border: none;
            font-size: 1rem;
            background: #1a1e2d;
            color: #fff;
            outline: none;
            box-shadow: 0 1px 4px #0002 inset;
        }
        input[type=text]::placeholder {
            color: #7a7f99;
        }
        button {
            background: linear-gradient(90deg, #3a8dde 60%, #5ec6fa 100%);
            color: #fff;
            border: none;
            border-radius: 8px;
            padding: 0 20px;
            font-size: 1rem;
            font-weight: 700;
            cursor: pointer;
            transition: background 0.2s;
        }
        button:hover {
            background: linear-gradient(90deg, #5ec6fa 60%, #3a8dde 100%);
        }
        .reset-btn {
            background: #2c3147;
            color: #b0b6c6;
            margin-top: 8px;
            width: 100%;
            padding: 10px 0;
            border-radius: 8px;
            font-size: 0.98rem;
            border: none;
            cursor: pointer;
            transition: background 0.2s;
        }
        .reset-btn:hover {
            background: #3a3f5c;
        }
        @media (max-width: 600px) {
            .container { max-width: 100vw; margin: 0; border-radius: 0; }
            .history { max-height: 60vh; }
        }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <span class="icon">🤖</span>
        <h2>OpenAI Sohbet Botu</h2>
    </div>
    <div class="history" id="history">
        {% for msg in history %}
            {% if msg.role == 'system' %}
                <div class="msg-system">Sistem: {{ msg.content }}</div>
            {% elif msg.role == 'user' %}
                <div class="msg-bubble msg-user">{{ msg.content }}</div>
            {% elif msg.role == 'assistant' %}
                <div class="msg-bubble msg-assistant">{{ msg.content }}</div>
            {% endif %}
        {% endfor %}
    </div>
    <form method="post" action="/">
        <input type="text" name="user_message" autofocus required placeholder="Mesajınızı yazın...">
        <button type="submit">Gönder</button>
    </form>
    <form method="post" action="/reset">
        <button type="submit" class="reset-btn">Sohbeti Sıfırla</button>
    </form>
</div>
<script>
    // Sohbet kutusunu en alta kaydır
    var historyDiv = document.getElementById('history');
    if(historyDiv){ historyDiv.scrollTop = historyDiv.scrollHeight; }
</script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    # chat_id session'da yoksa veya agents.chat_sessions'ta yoksa yeni oturum başlat
    if 'chat_id' not in session or session['chat_id'] not in agents.chat_sessions:
        session['chat_id'] = agents.create_chat()
    chat_id = session['chat_id']
    if request.method == 'POST':
        user_message = request.form.get('user_message')
        if user_message:
            try:
                agents.send_message(chat_id, user_message)
            except Exception as e:
                return f"Hata: {e}"
        return redirect(url_for('index'))
    history = agents.get_chat_history(chat_id)
    return render_template_string(HTML, history=history)

@app.route('/reset', methods=['POST'])
def reset():
    session.pop('chat_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 