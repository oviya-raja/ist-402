# Function Calling Guide: Connecting Local Functions to OpenAI Agent

## 🔗 How It Works: Cloud Agent → Local Functions

### The Challenge

- **OpenAI Agent Builder** runs in the cloud (platform.openai.com)
- **Your functions** might run on your local machine
- **Problem:** Cloud agent needs to call functions on your local machine

### The Solution: Webhooks + Tunneling

The agent calls your functions via HTTP webhooks. Your local machine needs to be accessible from the internet.

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────┐
│   OpenAI Agent (Cloud)           │
│   platform.openai.com            │
└──────────────┬──────────────────┘
               │
               │ HTTP Request (Function Call)
               │
┌──────────────▼──────────────────┐
│   Public URL (Tunnel)             │
│   ngrok.io / localtunnel.me       │
└──────────────┬──────────────────┘
               │
               │ Forward to Local
               │
┌──────────────▼──────────────────┐
│   Your Local Machine              │
│   localhost:8000                  │
│   Flask/FastAPI Server            │
└──────────────────────────────────┘
```

---

## 🚀 Method 1: Using ngrok (Recommended for Testing)

### Step 1: Install ngrok

```bash
# macOS
brew install ngrok

# Or download from https://ngrok.com
```

### Step 2: Create Local Function Server

**Example: Flask server (Python)**

```python
# local_function_server.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook/calendar_schedule', methods=['POST'])
def schedule_meeting():
    """Handle calendar scheduling function call from OpenAI agent"""
    data = request.json
    
    # Extract parameters from agent's function call
    title = data.get('title')
    date = data.get('date')
    duration = data.get('duration')
    
    # Your function logic here
    # (e.g., call Google Calendar API)
    result = {
        "success": True,
        "meeting_id": "12345",
        "message": f"Meeting '{title}' scheduled for {date}"
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
```

### Step 3: Start Local Server

```bash
python local_function_server.py
# Server running on http://localhost:8000
```

### Step 4: Create ngrok Tunnel

```bash
ngrok http 8000
```

**Output:**
```
Forwarding  https://abc123.ngrok.io -> http://localhost:8000
```

### Step 5: Configure Function in Agent Builder

1. Go to Agent Builder → Your Assistant → Tools
2. Add Function:
   ```json
   {
     "name": "schedule_meeting",
     "description": "Schedule a meeting in calendar",
     "parameters": {
       "type": "object",
       "properties": {
         "title": {"type": "string"},
         "date": {"type": "string"},
         "duration": {"type": "number"}
       }
     }
   }
   ```
3. Set webhook URL: `https://abc123.ngrok.io/webhook/calendar_schedule`

### Step 6: Test

- Agent calls function → ngrok forwards to localhost:8000 → Your function executes

---

## 🚀 Method 2: Using localtunnel (Alternative)

### Step 1: Install localtunnel

```bash
npm install -g localtunnel
```

### Step 2: Create Tunnel

```bash
lt --port 8000
```

**Output:**
```
your url is: https://random-name.loca.lt
```

### Step 3: Use URL in Agent Builder

- Set webhook URL: `https://random-name.loca.lt/webhook/calendar_schedule`

---

## 🚀 Method 3: Cloud Deployment (Production)

For production, deploy your functions to cloud services:

### Option A: Deploy to Cloud Run (Google Cloud)

```bash
# Deploy Flask app to Cloud Run
gcloud run deploy calendar-function \
  --source . \
  --platform managed \
  --region us-central1
```

**Result:** `https://calendar-function-xxx.run.app/webhook/calendar_schedule`

### Option B: Deploy to Railway/Render

1. Push code to GitHub
2. Connect to Railway/Render
3. Deploy automatically
4. Get public URL

### Option C: Deploy to AWS Lambda

- Serverless function
- Automatic scaling
- Pay per use

---

## 📋 Complete Example: Calendar Scheduling Function

### 1. Local Function (Python/Flask)

```python
# calendar_function.py
from flask import Flask, request, jsonify
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os

app = Flask(__name__)

@app.route('/webhook/schedule_meeting', methods=['POST'])
def schedule_meeting():
    """Handle meeting scheduling from OpenAI agent"""
    try:
        data = request.json
        
        # Extract parameters
        title = data.get('title', 'Meeting')
        date = data.get('date')
        duration = data.get('duration', 60)
        
        # Call Google Calendar API
        # (Implementation details here)
        
        result = {
            "success": True,
            "meeting_id": "cal_12345",
            "message": f"Meeting '{title}' scheduled successfully",
            "date": date,
            "duration_minutes": duration
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(port=8000, debug=True)
```

### 2. Start Server + Tunnel

```bash
# Terminal 1: Start Flask server
python calendar_function.py

# Terminal 2: Start ngrok tunnel
ngrok http 8000
```

### 3. Configure in Agent Builder

**Function Schema:**
```json
{
  "type": "function",
  "function": {
    "name": "schedule_meeting",
    "description": "Schedule a meeting in Google Calendar",
    "parameters": {
      "type": "object",
      "properties": {
        "title": {
          "type": "string",
          "description": "Meeting title"
        },
        "date": {
          "type": "string",
          "description": "Meeting date and time (ISO format)"
        },
        "duration": {
          "type": "number",
          "description": "Duration in minutes"
        }
      },
      "required": ["title", "date"]
    }
  }
}
```

**Webhook URL:** `https://abc123.ngrok.io/webhook/schedule_meeting`

### 4. Test

Ask agent: "Schedule a meeting called 'Team Standup' for tomorrow at 2pm for 30 minutes"

Agent will:
1. Call `schedule_meeting` function
2. Send request to ngrok URL
3. ngrok forwards to localhost:8000
4. Your function executes
5. Returns result to agent
6. Agent responds to user

---

## ⚠️ Important Notes

### For Local Development (Testing)

1. **ngrok/localtunnel are temporary**
   - URLs change each time you restart
   - Free tier has limitations
   - Good for testing only

2. **Keep tunnel running**
   - If tunnel stops, agent can't reach your function
   - Keep both server and tunnel running

3. **Security**
   - Local functions are exposed to internet
   - Use authentication if needed
   - Don't expose sensitive data

### For Production

1. **Deploy to cloud**
   - Use permanent URLs
   - Better reliability
   - Proper security

2. **Authentication**
   - Use API keys
   - Implement OAuth if needed
   - Secure your endpoints

---

## 🎯 For This Assignment

### Recommendation: Start Simple

**Option 1: Use Built-in Tools Only**
- ✅ No function calling needed
- ✅ No local deployment
- ✅ Everything in Agent Builder UI
- ✅ Simplest approach

**Option 2: Simple Function (If Needed)**
- Use ngrok for testing
- Document the setup
- Show screenshots of:
  - Local server running
  - ngrok tunnel active
  - Function working in agent

**Option 3: Cloud Deployment (Advanced)**
- Deploy to Railway/Render
- Permanent URL
- More professional
- Better for production

---

## 📋 Checklist for Function Calling

- [ ] Function implemented locally (Flask/FastAPI)
- [ ] Function tested locally (curl or Postman)
- [ ] ngrok tunnel created and running
- [ ] Function schema defined in Agent Builder
- [ ] Webhook URL configured in Agent Builder
- [ ] Function tested from agent
- [ ] Screenshots captured (server, tunnel, agent calling function)

---

## 🔍 Troubleshooting

### Problem: Agent can't reach function

**Solutions:**
- ✅ Check ngrok tunnel is running
- ✅ Verify webhook URL is correct
- ✅ Check local server is running
- ✅ Test function directly with curl

### Problem: Function returns error

**Solutions:**
- ✅ Check function logs
- ✅ Verify request format
- ✅ Test function independently
- ✅ Check authentication

### Problem: ngrok URL expired

**Solutions:**
- ✅ Restart ngrok (get new URL)
- ✅ Update webhook URL in Agent Builder
- ✅ Consider paid ngrok for static URL

---

## 📚 Resources

- **ngrok:** https://ngrok.com
- **localtunnel:** https://localtunnel.github.io/www/
- **OpenAI Function Calling:** https://platform.openai.com/docs/guides/function-calling
- **Flask:** https://flask.palletsprojects.com/
- **FastAPI:** https://fastapi.tiangolo.com/

---

## ✅ Summary

**How Cloud Agent Connects to Local Functions:**

1. **Agent calls function** → Sends HTTP request to webhook URL
2. **Tunnel (ngrok)** → Forwards request to localhost
3. **Local server** → Receives request, executes function
4. **Response** → Returns result through tunnel to agent

**Key Tools:**
- **ngrok** or **localtunnel** for tunneling
- **Flask** or **FastAPI** for local server
- **Agent Builder** for function configuration

**For Assignment:**
- Start with built-in tools (no function calling needed)
- If using functions, use ngrok for testing
- Document the setup clearly
- Show screenshots of the connection working

---

**Status:** ✅ Ready to implement function calling

