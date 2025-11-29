# Integration Points

## External Data Sources

### Company Job Posting Websites

Target companies are configured via CSV file (`target-companies.csv`). The agent reads company information from this file, including:
- Company name
- Careers URL
- Priority level
- Status (active/inactive)

**Default Companies (from CSV):**
- Cisco: https://careers.cisco.com/global/en
- SAP: https://jobs.sap.com/
- Google: https://careers.google.com/jobs/
- Apple: https://jobs.apple.com/
- Amazon: https://www.amazon.jobs/
- Tesla: https://www.tesla.com/careers

**CSV Format:**
```csv
company,careers_url,priority_level,status
Cisco,https://careers.cisco.com/global/en,1,active
Google,https://careers.google.com/jobs/,1,active
...
```

**Configuration Benefits:**
- Easy to add/remove companies without code changes
- Priority levels can be adjusted per company
- Companies can be temporarily disabled (status: inactive)
- Supports dynamic company list updates

**CSV Loading:**
- Agent reads CSV file at startup or on-demand
- Validates CSV format and required columns
- Filters companies by status (only processes active companies)
- Maps priority levels to analysis depth

**Example Usage:**
```python
# Agent loads companies from CSV
companies = load_companies_from_csv('target-companies.csv')
active_companies = [c for c in companies if c['status'] == 'active']
priority_1_companies = [c for c in active_companies if c['priority_level'] == '1']
```

### Knowledge Base
- Student profiles (skills, experience, education)
- Company information and job site structures
- Historical job posting data

---

## APIs and Services

### OpenAI Agent Builder
- **Purpose:** Agent orchestration and decision-making
- **Usage:** Core agent framework for workflow execution

### Web Scraping/Crawling Tools
- **Purpose:** Extract job postings from company websites
- **Tools:** Playwright, BeautifulSoup, or similar
- **Authentication:** Public websites (no auth required)

### Knowledge Base API
- **Purpose:** Profile matching and data retrieval
- **Format:** REST API or vector database
- **Authentication:** API key (if applicable)

### Analysis Engine
- **Purpose:** Fitment calculations and skill gap analysis
- **Implementation:** Custom logic or LLM-based analysis

---

## Data Exchange Formats

### Input Format (JSON)
```json
{
  "profile": {
    "skills": ["Python", "Java", "AWS"],
    "experience": "Entry-level",
    "education": "BS Computer Science",
    "location": "Remote"
  },
  "target_companies": {
    "priority_1": ["Cisco", "Google"],
    "priority_2": ["Apple"]
  }
}
```

### Output Format (JSON)
```json
{
  "jobs": [
    {
      "company": "Cisco",
      "title": "Software Engineer - New Grad",
      "fitment_percentage": 85,
      "matched_skills": ["Python", "Java"],
      "missing_skills": ["Networking basics"],
      "url": "https://..."
    }
  ]
}
```

---

## Authentication Methods

### Company Job Sites
- **Type:** Public access (no authentication required)
- **Access Method:** Direct HTTP/HTTPS requests
- **Rate Limiting:** Respect robots.txt and terms of service
- **User-Agent:** Set appropriate user-agent header

### Knowledge Base API
- **Type:** API key authentication (if applicable)
- **Method:** Bearer token in Authorization header
- **Format:** `Authorization: Bearer <api_key>`
- **Storage:** Store API key in environment variables
- **Example:**
  ```python
  headers = {
      'Authorization': f'Bearer {os.getenv("KNOWLEDGE_BASE_API_KEY")}',
      'Content-Type': 'application/json'
  }
  ```

### OpenAI Agent Builder
- **Type:** OpenAI API key
- **Method:** Configured in Agent Builder settings
- **Storage:** Secure storage in OpenAI platform
- **Access:** Automatic authentication for agent operations
- **Setup:** Add API key in Agent Builder → Settings → API Keys

### Environment Variables
- **Purpose:** Store sensitive credentials
- **Variables:**
  - `OPENAI_API_KEY`: OpenAI API key
  - `KNOWLEDGE_BASE_API_KEY`: Knowledge base API key (if applicable)
  - `TARGET_COMPANIES_CSV`: Path to CSV file (default: `docs/target-companies.csv`)
- **Security:** Never commit API keys to version control

---

## Error Handling Strategies

### Website Access Failures
- **Strategy:** Retry with exponential backoff (3 attempts)
- **Fallback:** Return cached data if available
- **User Notification:** Inform user of access issues

### Missing Data Scenarios
- **Strategy:** Use partial data when available
- **Fallback:** Request additional information from user
- **Validation:** Check required fields before processing

### API Timeout Handling
- **Strategy:** Set timeout limits (30 seconds per request)
- **Fallback:** Return partial results with timeout notification
- **Retry:** Automatic retry for transient failures

### Invalid Input Handling
- **Strategy:** Validate input format before processing
- **Error Messages:** Clear, actionable error messages
- **Suggestion:** Provide input format examples

---

**Status:** ✅ Complete  
**Last Updated:** 2025-11-29

