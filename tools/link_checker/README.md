# Link Checker

Recursively checks all links on a webpage using **100% FastMCP (Playwright MCP server)** with optional **AI analysis**.

## Key Features

- ✅ **100% FastMCP Client** - All browser operations via MCP tools (NO direct Playwright)
- ✅ **AI-Powered Analysis** (Optional) - Uses OpenAI GPT-4o-mini for intelligent insights
- ✅ **Type-Safe** - Full type hints with dataclasses
- ✅ **SOLID, DRY, KISS, YAGNI** - Clean architecture principles
- ✅ **Domain-Based Structure** - Organized by domain (checker, core, mcp, web, ai)

## Installation

### Required Dependencies

**For Playwright MCP (Core Functionality):**
```bash
pip install fastmcp          # FastMCP client library
npx playwright install chromium  # Install Playwright browsers for MCP server
```

**Note:** OpenAI is **NOT required** for Playwright MCP functionality. The tool works perfectly without it.

### Optional: AI Analysis

**For AI Analysis (Optional Feature):**
```bash
pip install openai           # Only needed if you want AI analysis
export OPENAI_API_KEY="your-api-key"  # Set API key for AI features
```

**Important:** 
- ✅ **Playwright MCP works WITHOUT OpenAI** - Link checking works fine without it
- ⚠️ **OpenAI is ONLY needed** if you want AI-powered analysis of results
- You can disable AI with `--no-ai` flag or `use_ai=False`

## Usage

### Command Line

```bash
# Basic usage
python -m tools.link_checker.cli https://oviya-raja.github.io/ist-402/

# Custom depth
python -m tools.link_checker.cli https://oviya-raja.github.io/ist-402/ --depth 3

# Without AI analysis
python -m tools.link_checker.cli https://oviya-raja.github.io/ist-402/ --depth 1 --no-ai

# Headless mode
python -m tools.link_checker.cli https://oviya-raja.github.io/ist-402/ --headless --no-ai

# Default URL (uses https://oviya-raja.github.io/ist-402/)
python -m tools.link_checker.cli
```

### Programmatic Usage

```python
from tools.link_checker import LinkChecker

# Create checker instance
checker = LinkChecker(
    base_url="https://oviya-raja.github.io/ist-402/",
    max_depth=2,
    use_ai=False
)

# Run check
summary, test_data = checker.check()

# Print results
checker.print_summary(summary, test_data)

# Access results
print(f"Passed: {len(summary.passed)}")
print(f"Failed: {len(summary.failed)}")
print(f"Warnings: {len(summary.warnings)}")
```

## Architecture

### Domain-Based Structure

```
tools/link_checker/
├── checker/              # Checker Domain - Main link checking logic
│   ├── engine.py        # LinkChecker class (core engine)
│   ├── formatter.py     # Output formatting
│   └── runner.py        # Entry point (main function)
│
├── core/                # Core Domain - Data models
│   └── models.py        # CheckSummary, TestData, LinkCheckResult
│
├── mcp/                 # MCP Domain - MCP operations
│   ├── client.py        # MCP client wrapper
│   ├── error_handler.py # Error handling
│   └── browser_lifecycle.py  # Browser management
│
├── web/                 # Web Domain - Web parsing
│   ├── url_parser.py    # URL utilities
│   └── html_parser.py   # HTML link extraction
│
└── ai/                  # AI Domain - AI analysis (OPTIONAL)
    ├── quality_analyzer.py  # AI analysis
    └── prompts.py       # AI prompts
```

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      CLI (cli.py)                           │
│                  Command-line Interface                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  Runner (checker/runner.py)                 │
│              Entry Point & Configuration                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Engine (checker/engine.py)                     │
│                  LinkChecker Class                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  • _check_links_on_page() - Recursive checking       │   │
│  │  • _check_single_link() - Individual link check      │   │
│  │  • _initialize_client() - MCP setup                  │   │
│  │  • _navigate_to_base() - Navigation                  │   │
│  └──────────────────────────────────────────────────────┘   │
└───────┬───────────────┬───────────────┬─────────────────────┘
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  MCP Domain  │ │  Web Domain  │ │  AI Domain   │
│              │ │              │ │  (Optional)  │
│ • client.py  │ │ • url_parser │ │ • analyzer   │
│ • error_     │ │ • html_      │ │ • prompts    │
│   handler    │ │   parser     │ │              │
│ • browser_   │ │              │ │              │
│   lifecycle  │ │              │ │              │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       └────────────────┼────────────────┘
                        │
                        ▼
              ┌─────────────────┐
              │  FastMCP Client │
              │  (Playwright)   │
              └─────────────────┘
```

### Data Flow

```
CLI → Runner → Engine → MCP Client → Playwright MCP Server → Browser
                              │
                              ├─→ Web Parser (extract links)
                              ├─→ URL Parser (resolve URLs)
                              └─→ AI Analyzer (optional analysis)
```

### 100% MCP Usage

All browser operations use MCP tools:
- `playwright_navigate`: Navigate to pages
- `playwright_get_visible_html`: Extract HTML content
- `playwright_evaluate`: Execute JavaScript
- `playwright_get`: Validate links

**No direct Playwright API calls** - everything goes through MCP.

### AI Integration (Optional)

- Uses OpenAI GPT-4o-mini for analysis
- Provides intelligent insights and recommendations
- **Disabled by default** if OpenAI not available
- **Not required** for core link checking functionality

## Dependencies Clarification

### ✅ Required for Core Functionality
- **FastMCP** (`pip install fastmcp`) - MCP client library
- **Playwright browsers** (`npx playwright install chromium`) - Browser runtime

### ⚠️ Optional (Only for AI Analysis)
- **OpenAI** (`pip install openai`) - Only needed if you want AI analysis
- **OPENAI_API_KEY** - Only needed if you want AI analysis

**Summary:** You can use Playwright MCP and check links **WITHOUT** OpenAI. OpenAI is only needed if you want AI-powered analysis of the results.

## Design Principles

- **KISS**: Simple, straightforward implementation
- **YAGNI**: Only features that are needed
- **SOLID**: Clean class design with domain separation
- **DRY**: No code duplication, reusable modules

## Code Quality

- ✅ All files <300 lines
- ✅ All methods <40 lines
- ✅ Domain-based organization
- ✅ 100% reusable utilities
- ✅ Type-safe with full type hints

## Error Handling

- Graceful handling of MCP server shutdown messages
- Clear error messages
- Proper exception propagation
- Automatic browser cleanup
