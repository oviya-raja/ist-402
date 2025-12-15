# Generative AI: Applications - n8n Automation Projects

## Table of Contents

1. [Introduction to n8n](#introduction-to-n8n)
2. [Project 1: Client Onboarding Automation](#project-1-client-onboarding-automation)
3. [Project 2: Automating Job Applications](#project-2-automating-job-applications)
4. [Project 3: AI WhatsApp Chatbot](#project-3-ai-whatsapp-chatbot)

---

# Introduction to n8n

## What is n8n?

n8n is a low-code automation tool that lets you connect APIs, cloud services, and logic without writing full apps.

**Key Features:**
- Visual programming (drag & drop logic)
- Connects to 300+ tools (Google, Slack, OpenAI, etc.)
- Great for automating multi-step workflows
- Can run locally or in the cloud
- Free and open source (for a limited time)

**Website:** https://cloud.n8n.io

---

## Local Setup of n8n

### Step 1: Install Docker

1. Download from https://docker.com
2. Confirm install:
   ```bash
   docker --version
   ```

### Step 2: Create Project Directory

```bash
mkdir n8n-project
cd n8n-project
```

### Step 3: Create Docker Compose File

Create a file named `docker-compose.yml` and add the following:

```yaml
version: '3'
services:
  n8n:
    image: n8nio/n8n
    restart: always
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=password
    volumes:
      - ~/.n8n:/home/node/.n8n
```

### Step 4: Start n8n

```bash
docker-compose up -d
```

### Step 5: Access n8n

n8n should now be running at: **http://localhost:5678**

---

# Project 1: Client Onboarding Automation

## Overview

Automate onboarding of new clients across platforms.

**When a form is submitted:**
- A Google Drive folder is created
- A new Slack channel is created
- A ClickUp list is generated
- A welcome email is prepared using OpenAI
- Client receives a Slack message

**Why this matters:** Saves time, ensures consistency, and gives clients a smooth onboarding experience.

---

## Tools Integrated in Workflow

| Tool | Purpose |
| --- | --- |
| n8n | Automates and connects all services visually |
| Google Drive API | Creates folders for each client |
| Slack API | Sets up communication channels |
| ClickUp API | Adds tasks for onboarding |
| OpenAI (GPT) | Writes welcome message content |

---

## Step 1: Connecting Google Drive in n8n

1. In n8n, go to **Credentials > New**
2. Choose **Google Drive OAuth2 API**
3. Connect your Google account (make sure to create an "Onboardings" folder first)
4. In the workflow, use the Google Drive node to:
   - Create folder
   - Set folder name = client's name or ID

**Troubleshooting:**
- If "Access Denied": make sure your OAuth client is set for external use and you're a test user.

---

## Step 2: Connecting ClickUp in n8n

1. Go to **ClickUp → Settings → API**
2. Generate a personal access token
3. In n8n, create a **ClickUp API Credential**
4. Use ClickUp nodes to:
   - Create a Folder
   - Create a List
   - Add Tasks

**Troubleshooting:**
- If ClickUp returns "Folder not found", make sure the folder doesn't already exist (ClickUp ignores duplicates)

---

## Step 3: Slack Setup in n8n

1. Go to **Slack API portal → Create App**
2. Add permissions:
   - `channels:write`
   - `chat:write`
   - `groups:write` (for private channels - optional)
3. Install app to your workspace
4. Copy OAuth Token into n8n credential setup

---

## Step 4: Using OpenAI in n8n

1. Create an OpenAI API key at https://platform.openai.com
2. In n8n:
   - Add **OpenAI API node**
   - Use ChatCompletion with system prompt: "You are a helpful onboarding assistant."

**Prompt Example:**
```
Create a warm welcome message for a new client named Windows, joining our platform today.
```

**Expected Output:**
```
"Welcome Windows! We're thrilled to have you on board. Let's get started!"
```

---

## Common Issues & Debugging

| Issue | Fix |
| --- | --- |
| "Missing OAuth scopes" | Add correct Slack/Google API scopes manually |
| ClickUp folder not created | Delete duplicate folder and rerun |
| OpenAI quota errors | Use gpt-3.5-turbo or upgrade plan |
| Slack can't post | Use correct channel ID and chat:write scope |
| Google Drive "Access Denied" | Ensure test user is added to Google project |

---

## Implementation Checklist

Use this checklist to ensure you complete all steps:

### Pre-Setup
- [ ] Docker installed and running
- [ ] n8n accessible at http://localhost:5678
- [ ] All required accounts created (Google, Slack, ClickUp, OpenAI)

### Google Drive Setup
- [ ] Google Cloud project created
- [ ] Google Drive API enabled
- [ ] OAuth credentials created (Client ID & Secret)
- [ ] OAuth consent screen configured
- [ ] "Onboardings" folder created in Google Drive
- [ ] Google Drive credential added in n8n

### ClickUp Setup
- [ ] ClickUp account created
- [ ] API token generated
- [ ] ClickUp credential added in n8n

### Slack Setup
- [ ] Slack app created
- [ ] Required scopes added (channels:write, chat:write)
- [ ] App installed to workspace
- [ ] Bot token copied
- [ ] Slack credential added in n8n

### OpenAI Setup
- [ ] OpenAI account created
- [ ] API key generated
- [ ] Payment method added
- [ ] OpenAI credential added in n8n

### Workflow Creation
- [ ] Trigger node added (Webhook or Manual)
- [ ] Google Drive node configured
- [ ] Slack node configured
- [ ] ClickUp node configured
- [ ] OpenAI node configured
- [ ] All nodes connected in sequence
- [ ] Workflow tested with sample data

### Testing
- [ ] Test workflow execution
- [ ] Verify Google Drive folder creation
- [ ] Verify Slack channel creation
- [ ] Verify ClickUp list/tasks creation
- [ ] Verify welcome message generation
- [ ] Verify Slack message delivery

## Detailed Workflow Steps

### Complete Workflow Structure

```
Trigger (Webhook/Manual)
    ↓
Google Drive: Create Folder
    ↓
ClickUp: Create Folder → Create List → Add Tasks
    ↓
OpenAI: Generate Welcome Message
    ↓
Slack: Create Channel → Send Message
```

### Node Configuration Details

**1. Trigger Node:**
- Type: Webhook (for form submissions) or Manual (for testing)
- Method: POST
- Path: `/webhook/client-onboarding`

**2. Google Drive Node:**
- Operation: Create
- Folder Name: `{{$json.clientName}}` or `{{$json.clientId}}`
- Parent Folder: "Onboardings" folder ID

**3. ClickUp Node (Folder):**
- Operation: Create Folder
- Name: `{{$json.clientName}}`
- Space ID: Your ClickUp space ID

**4. ClickUp Node (List):**
- Operation: Create List
- Name: "Onboarding Tasks"
- Folder ID: From previous node output

**5. ClickUp Node (Tasks):**
- Operation: Create Task
- Name: "Complete onboarding documentation"
- List ID: From previous node output
- Repeat for multiple tasks

**6. OpenAI Node:**
- Model: `gpt-4o-mini`
- System Prompt: "You are a helpful onboarding assistant."
- User Prompt: See [PROMPTS.md](./PROMPTS.md) for detailed prompts
- Temperature: 0.7
- Max Tokens: 200

**7. Slack Node (Channel):**
- Operation: Create Channel
- Channel Name: `client-{{$json.clientName}}`
- Is Private: false (or true for private channels)

**8. Slack Node (Message):**
- Operation: Post Message
- Channel: Channel ID from previous node
- Text: `{{$json.welcomeMessage}}` (from OpenAI output)

## What You'll Learn

- Design and deploy a multi-platform automation agent
- Understand OAuth credential setup and API rate limits
- Gain confidence using n8n as a low-code automation tool
- Successfully orchestrate multiple services (Slack, Google, ClickUp, OpenAI)
- Improve debugging across multiple APIs

---

# Project 2: Automating Job Applications

## Overview

**Problem:** Repetitive, time-consuming job applications

**Goal:** Fully automate job scraping, rating, and cover letter writing

**Tools:**
- n8n
- Ampify Web Scraper
- OpenAI API (GPT-4.0 mini)
- Google Sheets

---

## Why These Tools Were Chosen

| Tool | Reason |
| --- | --- |
| n8n | No-code/low-code workflow builder, free self-hosted or cloud version |
| Ampify | Reliable no-code scraper with webhook support (gives $5 signup bonus - ~100 jobs/day for a month) |
| GPT-4.0 Mini | Fast + cost-effective AI model |
| Google Sheets | Easy way to store and view data |

---

## Prerequisites: Create All Required Accounts

1. **n8n account** (cloud or self-hosted)
2. **Ampify account** (and request actor access)
3. **OpenAI account** + get API key
4. **Google Cloud setup** for Google Sheets API (optional if using webhook + sheets)

---

## Understanding Web Scraping

### What is Web Scraping?
Web scraping is the process of automatically extracting data from websites. A scraper program sends requests to a webpage, processes the HTML response, and extracts the relevant information — like job listings, product prices, or weather data.

### What are Actors?
Actors are serverless cloud programs ideal for web scraping and automation. They are easy to develop, share, and build upon. They can be started manually using an API or scheduler, and can be easily integrated with other apps.

---

## Step 1: Set Up a Trigger

A **Trigger** is the starting point of an automation workflow in n8n. It "listens" for a certain event — such as receiving a webhook, a new email, a scheduled time, or a new database entry — and starts the workflow when that event occurs.

**Configuration:**
- Set up a trigger for every day at 12 PM
- This way the automation will run everyday exactly at noon and extract all the information needed

---

## Step 2: Job Scraping using Ampify

### Finding Actors in Ampify

1. Sign in to Ampify (you get $5 balance on signup)
2. Search for online sources you could scrape information from
3. These actors tell you exactly how much they will charge for scraping
4. Use **Run actor Synchronously** to test the endpoint
5. Use the API token in the form of curl to copy directly into the n8n HTTP request

### HTTP Request Configuration

The HTTP Request node in n8n lets you make requests to any API endpoint using different HTTP methods (GET, POST, PUT, DELETE, etc.).

**Important Settings:**
- Connect Ampify to the HTTP request in n8n
- Use API endpoint and CLI for connecting
- In the edit JSON section, set **max rows to 10**
- If you don't set the max rows section, the Actor will scrape over 1000 listings at a time and cost a lot

### Output of HTTP Request

Once the connection is done, run the trigger once for testing to see what the output of HTTP request is going to be.
- You'll have your 10 jobs along with their description and title
- You can pin a single result to make sure your entire workflow works before running all 10 job postings

---

## Step 3: ChatGPT Models

The workflow uses **3 GPT models** for different tasks:

### Model 1: Extract Information

**Purpose:** Send job JSON to GPT to extract key information

**System Prompt:**
```
You are an intelligent bot that extracts key info from job posts.
```

**Output:** Cleaned, parsed job data including:
- Company name
- Job description
- Location
- If any required information is not provided on the job listing, it will return with 0

---

### Model 2: Relevance Rating

**Purpose:** Rate how well the job description matches your resume

**System Prompt:**
```
Rate how well this job matches the following resume.
```

**Input:** Include your resume and job details

**Output:** Score (0–5) with reasoning
- 3 points for skill matching
- 1 point each for being the right experience level and location

---

### Model 3: Generate Cover Letter

**Purpose:** Create a tailored cover letter for each job

**System Prompt:**
```
You're a perfect cover letter writer.
```

**Input:** Provide the model with the job listing and your resume

**Output:** Unique, tailored cover letter for each job posting that aligns your resume with the job description

---

## Step 4: Google Sheets Setup

### Part 1: Google Cloud Configuration

1. Go to **Google Cloud Console**
2. Sign in with your Google account
3. Create a New Project (or select an existing one)
4. Enable the Google Sheets API:
   - Go to: **APIs & Services → Library**
   - Search for **Google Sheets API**
   - Click **Enable**
5. Set Up OAuth Consent Screen:
   - Go to: **APIs & Services → OAuth consent screen**
   - Choose **External** for user type

### Part 2: Add Credentials in n8n

1. Choose **Google Sheets OAuth2 API**
2. Enter: Client ID and Client Secret from Google
3. Click **Connect**
4. A window will open → Sign in with your Google account → Accept permissions

### Part 3: Configure Google Sheets Node

The Google Sheet will keep all job postings based on unique links so that the same job doesn't get in the sheet again.

**Columns:**
- Company
- Job title
- Description
- Rating
- Cover Letter
- Link

---

## Final Output

The sheet gets updated everyday at noon with all the important information:
- Company name
- Job description
- Link to the job posting
- Rating (how well it matches your resume)
- Unique cover letter for each posting

**Usage:** All you need to do is click on the link to apply to job & copy and paste the cover letter along with your resume.

## Implementation Checklist

### Pre-Setup
- [ ] n8n running
- [ ] Ampify account created with API token
- [ ] OpenAI API key ready
- [ ] Google Cloud project with Sheets API enabled
- [ ] Google Sheet created with headers

### Ampify Configuration
- [ ] Actor found for job scraping
- [ ] API token obtained
- [ ] Actor ID noted
- [ ] Test run completed successfully

### Google Sheets Setup
- [ ] Google Sheets API enabled
- [ ] OAuth credentials created
- [ ] Sheet created with columns: Company, Job Title, Description, Rating, Cover Letter, Link
- [ ] Sheet ID copied
- [ ] Google Sheets credential added in n8n

### Resume Preparation
- [ ] Resume text prepared
- [ ] Resume stored as constant or variable in workflow
- [ ] Key skills and experience identified

### Workflow Creation
- [ ] Schedule trigger set (daily at 12 PM)
- [ ] HTTP Request node for Ampify configured
- [ ] OpenAI node 1: Extract Information
- [ ] OpenAI node 2: Relevance Rating
- [ ] OpenAI node 3: Generate Cover Letter
- [ ] Google Sheets node configured
- [ ] All nodes connected properly

### Testing
- [ ] Test with single job posting (pin result)
- [ ] Verify information extraction
- [ ] Verify rating calculation
- [ ] Verify cover letter generation
- [ ] Verify data written to Google Sheets
- [ ] Test with full workflow (10 jobs)

## Detailed Workflow Structure

```
Schedule Trigger (Daily 12 PM)
    ↓
HTTP Request: Ampify Job Scraping (maxRows: 10)
    ↓
Split In Batches (process each job)
    ↓
OpenAI: Extract Information
    ↓
OpenAI: Relevance Rating (with resume)
    ↓
IF Rating >= 3 (filter low-rated jobs)
    ↓
OpenAI: Generate Cover Letter
    ↓
Google Sheets: Append Row
```

### Node Configuration Details

**1. Schedule Trigger:**
- Trigger: Cron
- Cron Expression: `0 12 * * *` (daily at 12 PM)
- Or use: "Every Day at 12:00 PM"

**2. HTTP Request (Ampify):**
- Method: POST
- URL: `https://api.ampify.io/v2/actors/{ACTOR_ID}/run`
- Authentication: Header
- Header Name: `Authorization`
- Header Value: `Bearer {YOUR_API_TOKEN}`
- Body: JSON
```json
{
  "maxRows": 10,
  "startUrls": ["https://job-board-url.com"]
}
```

**3. Split In Batches:**
- Batch Size: 1 (process one job at a time)
- This allows processing each job individually

**4. OpenAI Node 1 (Extract):**
- Model: `gpt-4o-mini`
- System Prompt: See [PROMPTS.md](./PROMPTS.md)
- Input: `{{$json.jobData}}`
- Output: Structured JSON with company, title, location, etc.

**5. OpenAI Node 2 (Rating):**
- Model: `gpt-4o-mini`
- System Prompt: See [PROMPTS.md](./PROMPTS.md)
- Input: Job data + Resume
- Output: Rating (0-5) with reasoning

**6. IF Node (Filter):**
- Condition: `{{$json.rating}} >= 3`
- Only process jobs with rating 3 or higher

**7. OpenAI Node 3 (Cover Letter):**
- Model: `gpt-4o-mini` or `gpt-4`
- System Prompt: See [PROMPTS.md](./PROMPTS.md)
- Input: Job data + Resume + Rating
- Output: Tailored cover letter

**8. Google Sheets Node:**
- Operation: Append
- Spreadsheet ID: Your sheet ID
- Range: `Sheet1!A:F`
- Values: 
  - Company: `{{$json.companyName}}`
  - Job Title: `{{$json.jobTitle}}`
  - Description: `{{$json.description}}`
  - Rating: `{{$json.rating}}`
  - Cover Letter: `{{$json.coverLetter}}`
  - Link: `{{$json.applicationLink}}`

---

# Project 3: AI WhatsApp Chatbot

## Overview

This project automates conversations on WhatsApp by integrating an AI chatbot using n8n, GPT-4.0 Mini, and WhatsApp Cloud API.

The bot can interpret both **text and image inputs** and respond accordingly. It serves as a 24/7 assistant for customer support, education, or personal tasks.

**Key Benefits:**
- Instant replies powered by GPT-4.0 mini
- Cost-effective and fast inference
- Fully automated and scalable system

---

## What the Bot Can Do

- **Text Questions:** Answers factual, conversational, or task-based queries
- **Image Interpretation:** Generates captions or analyzes uploaded photos
- **Smart Replies:** Remembers previous prompts in a session
- **Multi-use:** Customer support, helpdesk, feedback system
- **Hands-free access:** Just chat on WhatsApp, no app needed

---

## Tools and Why They Were Chosen

| Tool | Reason |
| --- | --- |
| WhatsApp Cloud API | Official, reliable, supports text/image |
| GPT-4.0 Mini | Cost-effective, fast inference |
| n8n | Orchestrates the message → AI → reply flow |

---

## Prerequisites: Create All Required Accounts

### Meta Developer Account Setup

1. Go to https://developers.facebook.com/
2. Register App → Enable WhatsApp
3. Get:
   - Phone Number ID
   - Access Token
   - Webhook URL (from n8n)
4. Add a test phone number via Meta dashboard

### Configure n8n Webhook

1. Webhook node receives WhatsApp messages
2. Add fields for:
   - Text content
   - Media ID (if image sent)

---

## Step 1: Set Up WhatsApp Receiver

Configure using WhatsApp Business Cloud API:

1. Register app on Facebook for Developers
2. Set Webhook to receive messages and media
3. Integrate Access token and phone number ID into n8n
4. Triggers whenever a new message is received

**Note:** Due to API limitations, we could only use one trigger at a time.

---

## Step 2: Switch Node (Conditional Routing)

The **Switch node** lets you define multiple conditions and route the flow of the workflow depending on the value of a specific field. Instead of using multiple IF nodes, you can handle multiple cases in a cleaner and more efficient way.

**Logic:**
- If message has text → Send to GPT directly
- If message has image → Download → Analyze with GPT
- Else → Default message (error or fallback)

---

## Text Input Flow

### Processing Text Messages

Once a text message is received:
1. Message content is extracted
2. Sent to OpenAI GPT-4.0 Mini via HTTP Request node
3. AI generates a smart, relevant response
4. Message is sent back via WhatsApp

### AI Agent Configuration

The AI Agent has a simple memory that stores all past conversations.

**Configuration:**
- GPT-4.0 Mini is prompted with the user message
- Optional system prompt used to control tone/personality
- Temperature and max tokens configured for consistency
- Returned message is passed to the WhatsApp API node

**System Prompt:**
```
You are a helpful assistant called Helper AI.
Respond in a friendly tone and act like an assistant.
```

### Example Text Interaction

**Input:** "Can you tell me the gas price in Pennsylvania"

**Output:** "Sure, Mayank! As of the most recent data in July 2025, the average cost of regular gasoline in Pennsylvania is approximately $3.45 per gallon. Keep in mind that prices can vary depending on the city and specific gas station. Would you like information on premium or diesel fuel prices as well?"

---

## Image Input Flow

### Step 1: WhatsApp Get Image

- Receives image ID from the WhatsApp Webhook
- Retrieves media URL using WhatsApp Cloud API
- The image is temporarily stored in the form of JSON `image.id`
- Only JPG and PNG types currently supported

### Step 2: Image Downloader

The Image Downloader downloads an image from a URL, then processes it, saves it to a file system, uploads to cloud storage (like S3), sends over email, or passes it to another API.

**Process:**
1. Image media ID is converted to a downloadable link
2. n8n uses HTTP GET with bearer token
3. File is prepared for processing
4. Output is sent to the next step: "Analyze Image"

**Output:** A JPG/image type which is sent to GPT to analyze

### Step 3: GPT Model – Analyze Image

This GPT-4.0 mini model analyzes an image and gives output as instructed.

**Prompt:**
```
Describe this image in detail.
```

**Capabilities:**
- Supports general object detection
- Context inference
- Generates captions or best guesses

**Note:** Once the free credits are over, the only option is to pay.

### Example Image Interaction

**Input:** Picture of students having a Zoom meeting discussion of their final exam

**Output:** Detailed paragraph describing what the image contains

---

## WhatsApp Messenger Sender

The WhatsApp Messenger Send node lets you automate sending WhatsApp messages by connecting to a WhatsApp Business API account (not a personal WhatsApp account).

**Configuration:**
- Phone number: Grabbed from the initial text message
- Text body: Output from GPT that needs to be sent out through WhatsApp

---

## Complete Workflow Summary

```
WhatsApp Message Received
         ↓
    Switch Node
    /         \
Text           Image
   ↓              ↓
AI Agent    Get Image ID
   ↓              ↓
GPT Response  Download Image
   ↓              ↓
    \         Analyze Image
     \           /
      \         /
   WhatsApp Send Response
```

## Implementation Checklist

### Pre-Setup
- [ ] Meta Developer account created
- [ ] WhatsApp Business API access obtained
- [ ] Phone number verified
- [ ] OpenAI API key ready
- [ ] n8n webhook URL ready (or ngrok for local)

### Meta/WhatsApp Setup
- [ ] App created in Meta Developer Console
- [ ] WhatsApp product added
- [ ] Phone Number ID obtained
- [ ] Access Token obtained (temporary or permanent)
- [ ] Verify Token created
- [ ] Webhook URL configured in Meta dashboard
- [ ] Webhook verified successfully
- [ ] Test phone number added

### n8n Configuration
- [ ] Webhook node created and listening
- [ ] WhatsApp credential added (Phone Number ID + Access Token)
- [ ] OpenAI credential added
- [ ] Switch node configured
- [ ] Text processing branch configured
- [ ] Image processing branch configured
- [ ] WhatsApp Send node configured

### Workflow Creation
- [ ] Webhook trigger node
- [ ] Switch node (text vs image)
- [ ] Text branch: OpenAI → WhatsApp Send
- [ ] Image branch: Get Image → Download → Analyze → WhatsApp Send
- [ ] Error handling node (default case)

### Testing
- [ ] Test webhook receives messages
- [ ] Test text message handling
- [ ] Test image message handling
- [ ] Verify responses are sent
- [ ] Test error handling

## Detailed Workflow Structure

```
Webhook (POST /webhook/whatsapp)
    ↓
Extract Message Data
    ↓
Switch Node
    ├─ Case 1: Has Text → OpenAI Chat → WhatsApp Send
    ├─ Case 2: Has Image → Get Image URL → Download → OpenAI Vision → WhatsApp Send
    └─ Default: Error Message → WhatsApp Send
```

### Node Configuration Details

**1. Webhook Node:**
- Method: POST
- Path: `/webhook/whatsapp`
- Response Mode: "Last Node"
- Authentication: None (Meta verifies with token)

**2. Extract Data Node (Code/Set):**
Extract from webhook payload:
```javascript
{
  phoneNumber: $json.entry[0].changes[0].value.messages[0].from,
  messageId: $json.entry[0].changes[0].value.messages[0].id,
  messageText: $json.entry[0].changes[0].value.messages[0].text?.body,
  imageId: $json.entry[0].changes[0].value.messages[0].image?.id,
  messageType: $json.entry[0].changes[0].value.messages[0].type
}
```

**3. Switch Node:**
- Mode: Rules
- Rules:
  - Rule 1: `{{$json.messageType}} === "text"` → Output 1
  - Rule 2: `{{$json.messageType}} === "image"` → Output 2
  - Default: Output 3 (error)

**4. OpenAI Node (Text):**
- Model: `gpt-4o-mini`
- System Prompt: See [PROMPTS.md](./PROMPTS.md)
- Messages:
  - System: "You are a helpful assistant..."
  - User: `{{$json.messageText}}`
- Temperature: 0.7
- Max Tokens: 300

**5. HTTP Request (Get Image URL):**
- Method: GET
- URL: `https://graph.facebook.com/v18.0/{{$json.imageId}}`
- Authentication: Header
- Header: `Authorization: Bearer {WHATSAPP_ACCESS_TOKEN}`
- Response: Contains media URL

**6. HTTP Request (Download Image):**
- Method: GET
- URL: `{{$json.mediaUrl}}`
- Authentication: Header
- Header: `Authorization: Bearer {WHATSAPP_ACCESS_TOKEN}`
- Response Format: File

**7. OpenAI Node (Image Analysis):**
- Model: `gpt-4o-mini` or `gpt-4-vision-preview`
- System Prompt: See [PROMPTS.md](./PROMPTS.md)
- Messages:
  - User: 
    - Type: "text"
    - Content: "Describe this image in detail."
    - Type: "image_url"
    - Image URL: `{{$json.data}}` (base64 or URL)

**8. WhatsApp Send Node:**
- Phone Number: `{{$json.phoneNumber}}`
- Message: `{{$json.response}}` (from OpenAI)
- Use Credential: WhatsApp credential

**9. Error Handler (Default):**
- Message: "I'm sorry, I can only process text messages and images. Please try again."

---

# Summary

This guide covered three complete n8n automation projects:

1. **Client Onboarding Automation** - Automates folder creation, channel setup, task management, and welcome messages across Google Drive, Slack, ClickUp, and OpenAI.

2. **Job Application Automation** - Scrapes job listings, extracts information, rates relevance to your resume, generates custom cover letters, and stores everything in Google Sheets.

3. **AI WhatsApp Chatbot** - Creates a 24/7 AI assistant on WhatsApp that can handle both text and image inputs using GPT-4.0 Mini.

Each project demonstrates the power of n8n as a low-code automation platform and its ability to integrate multiple APIs and services into cohesive workflows.

---

# Quick Reference: Common Issues

| Issue | Fix |
| --- | --- |
| Missing OAuth scopes | Add correct Slack/Google API scopes manually |
| ClickUp folder not created | Delete duplicate folder and rerun |
| OpenAI quota errors | Use gpt-3.5-turbo or upgrade plan |
| Slack can't post | Use correct channel ID and chat:write scope |
| Google Drive "Access Denied" | Ensure test user is added to Google project |
| Ampify scraping too many results | Set max rows to 10 in JSON configuration |
| WhatsApp API limitations | Use one trigger at a time |
| Webhook not receiving messages | Check webhook URL is accessible, verify token matches |
| Docker port conflict | Change port in docker-compose.yml (e.g., 5679:5678) |
| n8n credential errors | Re-authenticate OAuth credentials |
| OpenAI rate limits | Add delays between requests, upgrade plan |
| Google Sheets permission errors | Ensure OAuth scopes include Sheets API |

---

# Additional Resources

## Documentation Files

- **[SETUP_GUIDE.md](./SETUP_GUIDE.md)** - Complete setup instructions for all services
- **[PROMPTS.md](./PROMPTS.md)** - Detailed AI prompt examples and configurations
- **[README.md](./README.md)** - Project overview and quick start guide

## Testing Workflows

### Before Production Deployment

1. **Test with Single Item:**
   - Use "Pin Data" feature in n8n
   - Test workflow with one item before processing batches

2. **Monitor API Usage:**
   - Check OpenAI usage dashboard
   - Monitor Ampify credits
   - Track API rate limits

3. **Error Handling:**
   - Add error handling nodes
   - Set up notifications for failures
   - Log errors for debugging

4. **Cost Optimization:**
   - Use `gpt-4o-mini` instead of `gpt-4` when possible
   - Set appropriate max tokens
   - Cache responses when applicable

## Next Steps

After completing these projects:

1. **Extend Functionality:**
   - Add more automation steps
   - Integrate additional services
   - Create custom error handling

2. **Optimize Workflows:**
   - Reduce API calls where possible
   - Add caching mechanisms
   - Improve error recovery

3. **Scale Up:**
   - Move to n8n cloud for reliability
   - Set up monitoring and alerts
   - Document your workflows

## Support & Community

- [n8n Community Forum](https://community.n8n.io/)
- [n8n Documentation](https://docs.n8n.io/)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [WhatsApp Business API](https://developers.facebook.com/docs/whatsapp)

---

**Happy Automating! 🚀**
