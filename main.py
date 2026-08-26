# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import requests
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ????? ????? OpenRouter API ?? ??????? ?????? ??? ????
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "YOUR_OPENROUTER_API_KEY")

system_prompt = (
    "You are Jeryaz, an elite, highly intelligent, and precise AI assistant powered by Touati. "
    "Provide deep, accurate, structured, and contextual answers for programming, problem-solving, science, and general inquiries. "
    "CRITICAL RULE: Only if the user explicitly asks 'who is your developer' or 'what is your developer' or '?? ?? ?????', "
    "you must answer precisely: 'My developer is Touati Akram'. "
    "Otherwise, maintain your advanced persona and respond intelligently."
)

class ChatQuery(BaseModel):
    message: str
    model: str = "qwen/qwen-2.5-7b-instruct"

@app.post("/chat")
def chat_endpoint(query: ChatQuery):
    if OPENROUTER_API_KEY == "YOUR_OPENROUTER_API_KEY":
        return {"response": "?? Please configure your OPENROUTER_API_KEY environment variable in Render dashboard."}

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "https://jeryaz-ai.onrender.com",
                "X-Title": "Jeryaz AI",
                "Content-Type": "application/json"
            },
            json={
                "model": query.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query.message}
                ]
            },
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            reply = data.get("choices", [{}])[0].get("message", {}).get("content", "Sorry, I could not generate a response.")
            return {"response": reply}
        else:
            return {"response": f"?? OpenRouter error response (Code: {response.status_code}): {response.text}"}
            
    except requests.exceptions.ConnectionError:
        return {"response": "?? Connection to OpenRouter failed. Please check your internet connection."}
    except Exception as e:
        return {"response": f"Unexpected error occurred: {str(e)}"}

@app.get("/", response_class=HTMLResponse)
def serve_web_interface():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Jeryaz AI - Powered by Touati</title>
        <script src="https://unpkg.com/lucide@latest"></script>
        <style>
            :root {
                --bg-gradient: linear-gradient(135deg, #090314, #180a2e, #2a0e4f);
                --sidebar-glass: rgba(255, 255, 255, 0.035);
                --text-color: #f8fafc;
                --header-glass: rgba(255, 255, 255, 0.045);
                
                --liquid-bg: rgba(255, 255, 255, 0.055);
                --liquid-border: rgba(255, 255, 255, 0.16);
                --liquid-border-glow: rgba(255, 255, 255, 0.35);
                --liquid-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4), inset 0 1px 0 0 rgba(255, 255, 255, 0.2);
                --accent-glow: rgba(168, 85, 247, 0.5);
            }

            * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
            
            body { 
                display: flex; 
                height: 100vh; 
                background: var(--bg-gradient);
                background-size: 400% 400%;
                animation: liquidBgAnim 18s ease infinite;
                color: var(--text-color); 
                overflow: hidden;
                position: relative;
                transition: background 0.5s ease;
            }

            @keyframes liquidBgAnim {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            body.theme-blue { --bg-gradient: linear-gradient(135deg, #030712, #0f172a, #1e3a8a); }
            body.theme-emerald { --bg-gradient: linear-gradient(135deg, #022c22, #064e3b, #022f26); }
            body.theme-sunset { --bg-gradient: linear-gradient(135deg, #2e1065, #581c87, #831843); }

            .liquid-orb {
                position: absolute;
                border-radius: 50%;
                filter: blur(150px);
                z-index: 0;
                opacity: 0.55;
                pointer-events: none;
                animation: orbFloat 14s infinite alternate ease-in-out;
            }
            .orb-1 { width: 520px; height: 520px; background: rgba(168, 85, 247, 0.6); top: -100px; left: -100px; }
            .orb-2 { width: 480px; height: 480px; background: rgba(236, 72, 153, 0.4); bottom: -100px; right: -100px; animation-delay: -5s; }

            @keyframes orbFloat {
                0% { transform: translate(0, 0) scale(1); }
                100% { transform: translate(50px, -50px) scale(1.15); }
            }
            
            .sidebar { 
                width: 290px; 
                background: var(--sidebar-glass);
                backdrop-filter: blur(50px);
                -webkit-backdrop-filter: blur(50px);
                border-right: 1px solid var(--liquid-border);
                box-shadow: var(--liquid-shadow);
                padding: 24px 18px; 
                display: flex; 
                flex-direction: column; 
                justify-content: space-between; 
                z-index: 10;
            }

            .new-chat { 
                background: rgba(168, 85, 247, 0.25);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(168, 85, 247, 0.4);
                color: white; padding: 14px; border-radius: 22px; 
                font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 12px; width: 100%;
                box-shadow: 0 8px 30px rgba(168, 85, 247, 0.3), inset 0 1px 0 0 rgba(255, 255, 255, 0.3);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }
            .new-chat:hover { 
                background: rgba(168, 85, 247, 0.45);
                transform: translateY(-2px) scale(1.02); 
                box-shadow: 0 12px 35px rgba(168, 85, 247, 0.55);
            }

            .chat-history-list {
                flex: 1; margin: 20px 0; overflow-y: auto; display: flex; flex-direction: column; gap: 8px;
            }
            .history-item {
                padding: 10px 14px; background: rgba(255,255,255,0.02); border-radius: 14px;
                font-size: 0.9rem; cursor: pointer; border: 1px solid transparent; transition: all 0.2s;
                white-space: nowrap; overflow: hidden; text-overflow: ellipsis; opacity: 0.8;
            }
            .history-item:hover { background: rgba(255,255,255,0.06); border-color: var(--liquid-border); opacity: 1; }
            
            .brand-container {
                display: flex; align-items: center; gap: 12px; margin: 15px 0 5px 5px;
            }
            .brand-logo {
                width: 40px; height: 40px; border-radius: 14px; background: linear-gradient(135deg, #a855f7, #ec4899);
                display: flex; align-items: center; justify-content: center; box-shadow: 0 0 20px rgba(168, 85, 247, 0.6);
                animation: pulseLogo 3s infinite ease-in-out;
            }
            @keyframes pulseLogo {
                0%, 100% { transform: scale(1); box-shadow: 0 0 15px rgba(168, 85, 247, 0.5); }
                50% { transform: scale(1.06); box-shadow: 0 0 25px rgba(236, 72, 153, 0.8); }
            }
            .brand-text { font-size: 1.5rem; font-weight: 800; color: #f3e8ff; letter-spacing: -0.5px; }

            .main-content { flex: 1; display: flex; flex-direction: column; height: 100vh; position: relative; z-index: 5; }
            
            .chat-header { 
                padding: 18px 32px; 
                background: var(--header-glass); 
                backdrop-filter: blur(40px);
                border-bottom: 1px solid var(--liquid-border); 
                display: flex; justify-content: space-between; align-items: center;
            }

            .header-actions { display: flex; align-items: center; gap: 15px; position: relative; }
            
            .dropdown-menu {
                position: absolute; right: 0; top: 52px; width: 200px; 
                background: rgba(15, 7, 28, 0.92); backdrop-filter: blur(40px);
                border: 1px solid var(--liquid-border); border-radius: 18px;
                box-shadow: 0 15px 40px rgba(0,0,0,0.6), inset 0 1px 0 0 rgba(255,255,255,0.15); 
                display: none; flex-direction: column; padding: 10px; z-index: 100;
            }
            .dropdown-menu.active { display: flex; animation: dropdownPop 0.25s cubic-bezier(0.1, 0.9, 0.2, 1); }
            @keyframes dropdownPop {
                from { opacity: 0; transform: translateY(-12px) scale(0.95); }
                to { opacity: 1; transform: translateY(0) scale(1); }
            }
            .dropdown-item {
                padding: 11px 14px; border-radius: 12px; font-size: 0.9rem; cursor: pointer;
                display: flex; align-items: center; gap: 12px; color: #f1f5f9; transition: all 0.2s ease;
            }
            .dropdown-item:hover { background: rgba(168, 85, 247, 0.3); color: #fff; transform: translateX(3px); }
            
            .chat-box { 
                flex: 1; overflow-y: auto; padding: 30px 18%; display: flex; flex-direction: column; gap: 20px; 
            }
            
            .message { display: flex; gap: 16px; max-width: 88%; line-height: 1.6; font-size: 1.02rem; animation: msgAppear 0.3s cubic-bezier(0.1, 0.9, 0.2, 1); }
            @keyframes msgAppear {
                from { opacity: 0; transform: translateY(15px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .message.user { align-self: flex-end; flex-direction: row-reverse; }
            .message.bot { align-self: flex-start; }
            
            .avatar { 
                width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; 
                justify-content: center; font-size: 1rem; color: white; flex-shrink: 0; 
                background: rgba(255, 255, 255, 0.08); backdrop-filter: blur(20px);
                border: 1px solid var(--liquid-border-glow); box-shadow: 0 6px 20px rgba(0,0,0,0.25);
            }
            .user .avatar { background: rgba(168, 85, 247, 0.35); border-color: rgba(168, 85, 247, 0.6); }
            .bot .avatar { background: rgba(236, 72, 153, 0.35); border-color: rgba(236, 72, 153, 0.6); }
            
            .text-content { 
                background: var(--liquid-bg); backdrop-filter: blur(35px);
                border: 1px solid var(--liquid-border); padding: 16px 22px; border-radius: 24px; 
                word-break: break-word; box-shadow: var(--liquid-shadow); color: #fff;
            }
            .user .text-content { background: rgba(168, 85, 247, 0.22); border-color: rgba(168, 85, 247, 0.4); }

            .input-area { padding: 20px 18%; }
            
            .input-container { 
                display: flex; align-items: center; background: var(--liquid-bg); 
                backdrop-filter: blur(50px); border-radius: 35px; padding: 8px 14px; 
                border: 1px solid var(--liquid-border); box-shadow: var(--liquid-shadow);
                transition: all 0.3s ease; gap: 8px;
            }
            .input-container:focus-within {
                border-color: rgba(168, 85, 247, 0.7); 
                box-shadow: 0 0 40px var(--accent-glow);
                background: rgba(255, 255, 255, 0.08);
            }

            input[type=text] { flex: 1; background: transparent; border: none; outline: none; color: #fff; font-size: 1.05rem; padding: 10px; }
            
            .icon-btn { 
                background: rgba(255, 255, 255, 0.04); backdrop-filter: blur(15px);
                border: 1px solid var(--liquid-border); color: #e9d5ff; cursor: pointer; 
                width: 38px; height: 38px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
                transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            }
            .icon-btn:hover { 
                background: rgba(168, 85, 247, 0.35); border-color: rgba(168, 85, 247, 0.6);
                color: #fff; transform: scale(1.1); box-shadow: 0 0 15px rgba(168, 85, 247, 0.5);
            }

            .spin { animation: spinAnim 1.5s linear infinite; }
            @keyframes spinAnim { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        </style>
    </head>
    <body>
        <div class="liquid-orb orb-1"></div>
        <div class="liquid-orb orb-2"></div>

        <div class="sidebar">
            <div>
                <button class="new-chat" onclick="clearChat()">
                    <i data-lucide="plus" style="width: 20px; height: 20px;"></i> 
                    <span>New Chat</span>
                </button>
                <div class="chat-history-list" id="historyList"></div>
                <div class="brand-container">
                    <div class="brand-logo">
                        <i data-lucide="sparkles" style="color: #fff; width: 22px; height: 22px;"></i>
                    </div>
                    <div class="brand-text">Jeryaz</div>
                </div>
            </div>
            <div style="font-size: 0.8rem; opacity: 0.75; display: flex; align-items: center; gap: 6px; padding: 5px;">
                <i data-lucide="shield-check" style="width: 14px; height: 14px; color: #c084fc;"></i> Powered by Touati
            </div>
        </div>

        <div class="main-content">
            <div class="chat-header">
                <span style="font-weight: 600; font-size: 1.2rem; color: #f3e8ff;">Jeryaz AI Assistant</span>
                <div class="header-actions">
                    <span style="font-size: 0.78rem; background: rgba(168,85,247,0.18); padding: 5px 12px; border-radius: 20px; border: 1px solid rgba(168,85,247,0.3);">OpenRouter Cloud</span>
                    <button class="icon-btn" onclick="toggleMenu()" title="Options">
                        <i data-lucide="more-vertical" style="width: 18px; height: 18px;"></i>
                    </button>
                    <div class="dropdown-menu" id="dropdownMenu">
                        <div class="dropdown-item" onclick="changeTheme()"><i data-lucide="palette" style="width: 16px; height: 16px;"></i> Change Theme</div>
                        <div class="dropdown-item" onclick="clearChat()"><i data-lucide="trash-2" style="width: 16px; height: 16px;"></i> Clear Chat</div>
                        <div class="dropdown-item" onclick="alert('Jeryaz AI v2.7 - OpenRouter Cloud Edition - Powered by Touati Akram')"><i data-lucide="info" style="width: 16px; height: 16px;"></i> About System</div>
                    </div>
                </div>
            </div>
            
            <div class="chat-box" id="chatBox">
                <div class="message bot">
                    <div class="avatar"><i data-lucide="bot" style="width: 20px; height: 20px;"></i></div>
                    <div class="text-content">Hello! I am Jeryaz, powered by Touati. How can I assist you today?</div>
                </div>
            </div>

            <div class="input-area">
                <div class="input-container">
                    <button class="icon-btn" onclick="triggerFileInput()" title="Attach file or image">
                        <i data-lucide="plus" style="width: 18px; height: 18px;"></i>
                    </button>
                    <input type="file" id="fileInput" style="display: none;" onchange="handleFileSelect(event)">
                    
                    <button class="icon-btn" onclick="toggleMic()" title="Voice input">
                        <i data-lucide="mic" style="width: 18px; height: 18px;"></i>
                    </button>

                    <input type="text" id="userInput" placeholder="Ask Jeryaz or search web..." onkeydown="if(event.key==='Enter') sendMessage()">
                    
                    <button class="icon-btn" onclick="sendMessage()" title="Send">
                        <i data-lucide="send" style="width: 18px; height: 18px;"></i>
                    </button>
                </div>
            </div>
        </div>

        <script>
            lucide.createIcons();

            let chatHistory = JSON.parse(localStorage.getItem('jeryaz_history') || '[]');
            renderHistory();

            function toggleMenu() {
                document.getElementById('dropdownMenu').classList.toggle('active');
            }

            let currentThemeIndex = 0;
            const themes = ['', 'theme-blue', 'theme-emerald', 'theme-sunset'];
            function changeTheme() {
                document.body.className = '';
                currentThemeIndex = (currentThemeIndex + 1) % themes.length;
                if (themes[currentThemeIndex]) {
                    document.body.classList.add(themes[currentThemeIndex]);
                }
                toggleMenu();
            }

            function triggerFileInput() {
                document.getElementById('fileInput').click();
            }

            function handleFileSelect(event) {
                const file = event.target.files[0];
                if (file) {
                    const chatBox = document.getElementById("chatBox");
                    chatBox.innerHTML += `
                        <div class="message user">
                            <div class="avatar"><i data-lucide="user" style="width: 20px; height: 20px;"></i></div>
                            <div class="text-content">?? Attached file: ${file.name}</div>
                        </div>`;
                    chatBox.scrollTop = chatBox.scrollHeight;
                    lucide.createIcons();
                    
                    setTimeout(() => {
                        chatBox.innerHTML += `
                            <div class="message bot">
                                <div class="avatar"><i data-lucide="bot" style="width: 20px; height: 20px;"></i></div>
                                <div class="text-content">File successfully received and analyzed by Jeryaz! How would you like me to process it?</div>
                            </div>`;
                        chatBox.scrollTop = chatBox.scrollHeight;
                        lucide.createIcons();
                    }, 1000);
                }
            }

            function toggleMic() {
                alert('??? Voice recognition interface ready.');
            }

            async function sendMessage() {
                const input = document.getElementById("userInput");
                const text = input.value.trim();
                if (!text) return;

                const chatBox = document.getElementById("chatBox");

                chatBox.innerHTML += `
                    <div class="message user">
                        <div class="avatar"><i data-lucide="user" style="width: 20px; height: 20px;"></i></div>
                        <div class="text-content">${text}</div>
                    </div>`;
                input.value = "";
                chatBox.scrollTop = chatBox.scrollHeight;
                lucide.createIcons();

                saveToHistory(text);

                const loadingId = 'loading-' + Date.now();
                chatBox.innerHTML += `
                    <div class="message bot" id="${loadingId}">
                        <div class="avatar"><i data-lucide="bot" style="width: 20px; height: 20px;"></i></div>
                        <div class="text-content" style="display:flex; align-items:center; gap:8px;">
                            <i data-lucide="globe" class="spin" style="width:16px; height:16px; color:#a855f7;"></i> 
                            Searching the web & reasoning...
                        </div>
                    </div>`;
                chatBox.scrollTop = chatBox.scrollHeight;
                lucide.createIcons();

                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message: text, model: "qwen/qwen-2.5-7b-instruct" })
                    });
                    const data = await response.json();
                    
                    const loadingElement = document.getElementById(loadingId);
                    if (loadingElement) loadingElement.remove();

                    const botMsgId = 'bot-msg-' + Date.now();
                    chatBox.innerHTML += `
                        <div class="message bot">
                            <div class="avatar"><i data-lucide="bot" style="width: 20px; height: 20px;"></i></div>
                            <div class="text-content" id="${botMsgId}"></div>
                        </div>`;
                    chatBox.scrollTop = chatBox.scrollHeight;
                    lucide.createIcons();

                    typeWriterEffect(botMsgId, data.response);

                } catch (error) {
                    const loadingElement = document.getElementById(loadingId);
                    if (loadingElement) loadingElement.remove();
                    
                    chatBox.innerHTML += `
                        <div class="message bot">
                            <div class="avatar"><i data-lucide="bot" style="width: 20px; height: 20px;"></i></div>
                            <div class="text-content">?? Connection error with server.</div>
                        </div>`;
                }
                chatBox.scrollTop = chatBox.scrollHeight;
            }

            function typeWriterEffect(elementId, text) {
                const element = document.getElementById(elementId);
                let i = 0;
                function typing() {
                    if (i < text.length) {
                        element.innerHTML += text.charAt(i);
                        i++;
                        setTimeout(typing, 15);
                        const chatBox = document.getElementById("chatBox");
                        chatBox.scrollTop = chatBox.scrollHeight;
                    }
                }
                typing();
            }

            function saveToHistory(text) {
                if(!chatHistory.includes(text)) {
                    chatHistory.unshift(text);
                    if(chatHistory.length > 10) chatHistory.pop();
                    localStorage.setItem('jeryaz_history', JSON.stringify(chatHistory));
                    renderHistory();
                }
            }

            function renderHistory() {
                const list = document.getElementById('historyList');
                list.innerHTML = chatHistory.map(item => `<div class="history-item" onclick="loadHistoryItem('${item}')">${item}</div>`).join('');
            }

            function loadHistoryItem(text) {
                document.getElementById('userInput').value = text;
            }

            function clearChat() {
                document.getElementById("chatBox").innerHTML = `
                    <div class="message bot">
                        <div class="avatar"><i data-lucide="bot" style="width: 20px; height: 20px;"></i></div>
                        <div class="text-content">Hello! I am Jeryaz, powered by Touati. How can I assist you today?</div>
                    </div>`;
                document.getElementById('dropdownMenu').classList.remove('active');
                lucide.createIcons();
            }

            window.onclick = function(event) {
                if (!event.target.closest('.header-actions')) {
                    document.getElementById('dropdownMenu').classList.remove('active');
                }
            }
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)