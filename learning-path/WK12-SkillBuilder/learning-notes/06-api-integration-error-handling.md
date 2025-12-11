# API Integration & Error Handling Patterns

## Course Context
**Concepts:** External API Integration, Error Handling, Production Patterns  
**Related Weeks:** W06 (Safety and Guardrails)

---

## 1. API Integration Architecture

### Multi-API Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│                    API INTEGRATION LAYER                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                APIIntegrationManager                       │ │
│  │  (Unified interface for all external APIs)                 │ │
│  └────────────────────────┬───────────────────────────────────┘ │
│                           │                                      │
│           ┌───────────────┼───────────────┐                     │
│           │               │               │                     │
│           ▼               ▼               ▼                     │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │   NewsAPI    │ │  OpenAI      │ │   OpenAI     │            │
│  │  (Optional)  │ │  Embeddings  │ │  Web Search  │            │
│  └──────────────┘ └──────────────┘ └──────────────┘            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Custom Exception Class

### Why Custom Exceptions?

| Benefit | Description |
|---------|-------------|
| **Specificity** | Distinguish API errors from other exceptions |
| **Handling** | Catch API errors separately |
| **Context** | Include API-specific error information |
| **Clarity** | Clear error hierarchy |

### Error Handling Flow

```
API Call
    │
    ▼
┌─────────────────┐
│ Try Operation   │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
 Success   Failure
    │         │
    ▼         ▼
┌────────┐ ┌──────────────┐
│ Return │ │ Raise        │
│ Result │ │ APIError     │
└────────┘ └──────┬───────┘
                  │
                  ▼
         ┌─────────────────┐
         │ Catch & Handle  │
         │ • Log error     │
         │ • Show message  │
         │ • Fallback      │
         └─────────────────┘
```

---

## 3. API Client Initialization

### Initialization Checklist

```
┌─────────────────────────────────────────┐
│        API Initialization Flow          │
├─────────────────────────────────────────┤
│                                         │
│  1. Check package availability          │
│     └─► OPENAI_AVAILABLE check         │
│                                         │
│  2. Check API key                       │
│     └─► Environment variable           │
│     └─► Constructor parameter          │
│                                         │
│  3. Initialize client                   │
│     └─► Try/catch for errors           │
│     └─► Log success/failure            │
│                                         │
│  4. Set client to None on failure       │
│     └─► Allows graceful checks later   │
│                                         │
└─────────────────────────────────────────┘
```

---

## 4. Availability Checking Pattern

### Availability Check Flow

```
Check API Availability
    │
    ▼
┌─────────────────┐
│ Client Exists?  │
│ API Key Set?    │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
   Yes       No
    │         │
    ▼         ▼
┌────────┐ ┌──────────────┐
│Available│ │ Not Available│
│         │ │ Show warning │
└─────────┘ └──────────────┘
```

### Why This Pattern?

1. **User Feedback**: Clear status in UI
2. **Graceful Degradation**: Don't break if API unavailable
3. **Feature Toggling**: Enable/disable features based on availability
4. **Debugging**: Easy to identify configuration issues

---

## 5. API Call with Error Handling

### Error Handling Layers

```
┌─────────────────────────────────────────────────────────────┐
│                  ERROR HANDLING LAYERS                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Layer 1: Pre-condition Check                               │
│  └─► Check API key before making request                    │
│                                                              │
│  Layer 2: Request Timeout                                   │
│  └─► timeout=10 prevents hanging                            │
│                                                              │
│  Layer 3: HTTP Status Check                                 │
│  └─► response.raise_for_status()                            │
│                                                              │
│  Layer 4: Specific Exception Handling                       │
│  └─► requests.exceptions.RequestException                   │
│                                                              │
│  Layer 5: Catch-all Exception                               │
│  └─► Exception for unexpected errors                        │
│                                                              │
│  Layer 6: Custom Exception Wrapping                         │
│  └─► Wrap in APIError with context                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. API Call Logging

### Logging Strategy

| When | What to Log |
|------|-------------|
| **Before Call** | API name, parameters |
| **After Success** | Status, result count/size |
| **After Failure** | Error type, error message |
| **Always** | Timestamp (automatic) |

### Logging Flow

```
API Call Start
    │
    ▼
┌─────────────────┐
│ Log: Requesting │
│ API: {name}     │
│ Params: {...}   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Execute Call    │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
 Success   Failure
    │         │
    ▼         ▼
┌────────┐ ┌──────────────┐
│ Log:   │ │ Log:        │
│ Success│ │ Failed      │
│ Count  │ │ Error       │
└────────┘ └──────────────┘
```

---

## 7. Response Parsing with Fallbacks

### Parsing Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                   PARSING STRATEGY                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Primary Parsing                                         │
│     • Split by logical delimiters                           │
│     • Extract structured fields (URL, date, location)       │
│     • Use regex patterns for each field                     │
│                                                              │
│  2. Validation                                              │
│     • Check minimum content length                          │
│     • Verify required fields exist                          │
│     • Skip invalid entries                                  │
│                                                              │
│  3. Fallback Parsing                                        │
│     • If primary fails, use simpler approach                │
│     • Split by paragraphs                                   │
│     • Use first line as title                               │
│                                                              │
│  4. Defaults                                                │
│     • Ensure all required fields have values                │
│     • Use sensible defaults for missing data                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 8. Manager Pattern

### Manager Pattern Benefits

| Benefit | Description |
|---------|-------------|
| **Single Entry Point** | One class to access all APIs |
| **Abstraction** | Hide individual API complexity |
| **Coordination** | Combine data from multiple sources |
| **Configuration** | Centralized API setup |

### Manager Flow

```
User Request
    │
    ▼
┌─────────────────┐
│ API Manager     │
│ (Unified)       │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
   News    Web Search
    │         │
    ▼         ▼
┌─────────────────┐
│ Combine Results │
│ Format Context  │
└─────────────────┘
```

---

## 9. Environment Variable Management

### Environment Variable Best Practices

```
┌─────────────────────────────────────────────────────────────┐
│              ENVIRONMENT VARIABLE BEST PRACTICES             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. .env File                                               │
│     OPENAI_API_KEY=sk-...                                   │
│     NEWS_API_KEY=...                                        │
│                                                              │
│  2. .gitignore                                              │
│     .env  # Never commit API keys!                          │
│                                                              │
│  3. Example File                                            │
│     .env.example with dummy values                          │
│                                                              │
│  4. Load Priority                                           │
│     a) Constructor parameter                                │
│     b) Environment variable                                 │
│     c) Default value (if appropriate)                       │
│                                                              │
│  5. Validation                                              │
│     Check at startup, not at call time                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 10. Error Display in UI

### User-Friendly Error Handling

| Principle | Implementation |
|-----------|----------------|
| **Clear Message** | What went wrong |
| **Actionable** | How to fix it |
| **Non-Technical** | Avoid stack traces in UI |
| **Graceful Stop** | `st.stop()` prevents partial rendering |

### Error Display Flow

```
Error Occurs
    │
    ▼
┌─────────────────┐
│ Catch Exception │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Log Error       │
│ (Technical)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Show User       │
│ Friendly Message│
│ • What happened │
│ • How to fix    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Stop Execution  │
│ (Prevent crash) │
└─────────────────┘
```

---

## 11. Timeout Handling

### Why Timeouts Matter

```
Without Timeout:
┌─────────────────────────────────────────────────────────────┐
│  User clicks button                                          │
│       │                                                      │
│       ▼                                                      │
│  API call starts... (server is slow/down)                   │
│       │                                                      │
│       │ ← User waits... and waits... and waits...           │
│       │                                                      │
│       ▼                                                      │
│  Eventually: Connection reset / Browser timeout              │
└─────────────────────────────────────────────────────────────┘

With Timeout (10 seconds):
┌─────────────────────────────────────────────────────────────┐
│  User clicks button                                          │
│       │                                                      │
│       ▼                                                      │
│  API call starts... (server is slow/down)                   │
│       │                                                      │
│       │ ← 10 seconds max                                    │
│       │                                                      │
│       ▼                                                      │
│  Timeout exception → Show error → User can retry            │
└─────────────────────────────────────────────────────────────┘
```

---

## 12. Key Takeaways

| Concept | What I Learned |
|---------|----------------|
| **Custom Exceptions** | APIError for specific error handling |
| **Initialization Checks** | Validate API keys at startup |
| **Availability Pattern** | `is_available()` method for UI feedback |
| **Logging** | Log API calls for debugging |
| **Timeouts** | Prevent hanging requests |
| **Fallback Parsing** | Multiple strategies for unreliable data |
| **Manager Pattern** | Unified interface for multiple APIs |
| **User-Friendly Errors** | Clear messages with actionable advice |

---

## Error Handling Checklist

```
□ Custom exception class defined
□ Pre-condition checks before API calls
□ Timeout set on all HTTP requests
□ Specific exception handling (not just catch-all)
□ Logging at each stage (start, success, failure)
□ User-friendly error messages in UI
□ Availability checking pattern implemented
□ Fallback strategies for unreliable data
□ Environment variables properly loaded
□ API keys validated at initialization
```

---

## Related Concepts

- [LangChain Integration](./04-langchain-integration.md) - OpenAI API usage
- [RAG Pipeline](./05-rag-pipeline.md) - Using external context
- [Project Overview](./01-project-overview.md) - Architecture context
