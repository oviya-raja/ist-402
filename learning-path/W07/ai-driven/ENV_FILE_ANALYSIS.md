# .env File Analysis
## Which .env File is Being Used

**Date:** 2025-11-29

---

## 🔍 Findings

### .env File Location
- **Path:** `/Users/rajasoun/workspace/personal/oviya/ist-402/.env`
- **Status:** ✅ Exists and readable
- **Contains:** `OPENAI_API_KEY=sk-proj-dGBZODC9M2Ci...`

### ⚠️ CRITICAL ISSUE: Environment Variable Override

**Problem:**
- The `.env` file contains: `sk-proj-dGBZODC9M2Ci...`
- But the **shell environment** has: `sk-proj-N5vzWc8bPpz_...` set
- **Environment variables take precedence** over `.env` file!
- Therefore, scripts are using the **environment variable**, NOT the `.env` file

**Evidence:**
```
.env file shows:     sk-proj-dGBZODC9M2Ci...
Environment shows:   sk-proj-N5vzWc8bPpz_...
Scripts use:         sk-proj-N5vzWc8bPpz_... (from environment)
```

---

## 📋 dotenv Loading Order (Priority)

1. **Environment variables** (HIGHEST PRIORITY) ← Currently active
2. `.env` file in current directory
3. `.env` file in parent directories
4. `.env` file specified in `load_dotenv()`

---

## ✅ Solution

### Option 1: Unset Environment Variable (Recommended)

**Remove the environment variable so `.env` file is used:**

```bash
# Check if set
echo $OPENAI_API_KEY

# Unset it (for current session)
unset OPENAI_API_KEY

# Or remove from shell config files
# Check these files:
# - ~/.zshrc
# - ~/.bashrc
# - ~/.bash_profile
# - ~/.profile
```

Then scripts will use the `.env` file value.

### Option 2: Update Environment Variable

**Update the environment variable to match browser account:**

```bash
export OPENAI_API_KEY=sk-proj-... (key from browser account)
```

### Option 3: Update .env File

**Update `.env` file to match what you want to use:**

```bash
cd /Users/rajasoun/workspace/personal/oviya/ist-402
# Edit .env file
# Change OPENAI_API_KEY to the browser account's key
```

---

## 🔍 How to Check

**Check which API key is actually being used:**

```bash
cd deliverables/1-functional-agent/scripts
python3 -c "
from utils import load_env, get_api_key
load_env()
key = get_api_key()
print(f'API Key being used: {key[:20]}...')
"
```

**Check environment variable:**

```bash
echo $OPENAI_API_KEY
```

**Check .env file:**

```bash
cd /Users/rajasoun/workspace/personal/oviya/ist-402
grep OPENAI_API_KEY .env | grep -v "^#"
```

---

## 📝 Current Status

| Source | API Key | Status |
|--------|---------|--------|
| `.env` file | `sk-proj-dGBZODC9M2Ci...` | ❌ Not being used |
| Environment variable | `sk-proj-N5vzWc8bPpz_...` | ✅ **Currently active** |
| Browser account | Unknown (need to get) | ⚠️ Need to match |

---

## 🎯 Recommended Action

1. **Get API key from browser account:**
   - Go to: https://platform.openai.com/api-keys
   - Find "W07-Assignment" key
   - Copy the full key

2. **Update `.env` file:**
   ```bash
   cd /Users/rajasoun/workspace/personal/oviya/ist-402
   # Edit .env and update OPENAI_API_KEY
   ```

3. **Unset environment variable:**
   ```bash
   unset OPENAI_API_KEY
   ```

4. **Verify:**
   ```bash
   cd deliverables/1-functional-agent/scripts
   python3 verify_account_match.py
   ```

5. **Recreate assistant:**
   ```bash
   python3 repeat_phase2.py
   ```

---

**Status:** Environment variable is overriding .env file  
**Next Step:** Unset environment variable or update both to match browser account

