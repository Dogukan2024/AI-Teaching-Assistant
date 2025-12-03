# AI Lab – Flask + Socket.IO Streaming Chat with Token-Based Tiers

This project is a **Flask web application** that provides a real-time AI chat interface powered by **Socket.IO**, **SQLite**, and **OpenAI's streaming API**.  
Each user message consumes a coin from one of three tiers:

- **Gold** – highest assistance (direct solutions)
- **Silver** – intermediate guidance (conceptual help)
- **Copper** – basic help (debugging tips)

The selected coin tier determines the AI assistant's behavior and response detail.

---

## 🚀 Features

### 🔐 User Authentication
- User registration & login  
- Password hashing via Werkzeug  
- Session-based authentication  

### 🪙 Coin Economy
- Users have balances for **gold**, **silver**, and **copper** coins  
- Asking a question deducts 1 coin from the selected tier  
- Error messages for low coins, invalid messages, or not logged in  

### 🤖 OpenAI Integration
- Uses **OpenAI gpt-4o** with streaming enabled  
- Tier-based system instructions (bronze/silver/gold modes)  
- Real-time token streaming  

### ⚡ Real-Time Chat
- Built with Flask-SocketIO  
- Streams AI responses back to the client chunk by chunk  
- Clean event system: `stream`, `done`, `error`  

### 🗄 Database
- SQLite for user accounts + coin balances  
- CLI command: `flask init-db`  

---

## 📂 Project Structure

```
AIlab_test/
│
├── __init__.py            # Flask app factory + Socket.IO
├── aiAPI.py               # OpenAI API integration + streaming
├── auth.py                # User register/login/logout
├── db.py                  # SQLite helpers + schema setup
├── main.py                # Message handling, coin deduction, AI pipeline
├── warnings.py            # System warning helpers
└── templates/             # HTML templates
```

---

## 🧠 How It Works

1. User logs in  
2. User sends a Socket.IO message with:
   - content  
   - selected coin tier  
3. Server validates:
   - user session  
   - message format  
   - remaining coins  
4. Deducts a coin  
5. Sends request to OpenAI with tier-specific instructions  
6. Streams AI response back to the client using:
   - `{ type: "stream" }`
   - `{ type: "done" }`  



---

## 🛠 Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/AIlab_test.git
cd AIlab_test
```

### 2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize the database
```bash
flask --app AIlab_test init-db
```

### 5. Run the application
```bash
flask --app AIlab_test run
```


## 🔌 Socket.IO Message Structure

### Client → Server
```json
{
  "type": "message",
  "content": "Explain async functions.",
  "selected_coin": "gold"
}
```

## ⚙ Setting the OpenAI API Key

Edit this line inside `aiAPI.py`:
```python
API_KEY = "your-api-key-here"
```


## 🧭 Future Improvements

- Admin panel for editing coins  
- Improved frontend chat UI 
- Better message validation  



