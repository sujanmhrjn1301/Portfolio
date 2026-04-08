# GitHub Integration Setup Guide

## Overview
GitHub repository integration has been added as an **optional feature button**! Users can now click a "Projects" button near the search bar to view your latest repositories with detailed information including stars, languages, topics, and descriptions.

## How It Works

### 🚀 Features
- **On-Demand Loading**: Click the GitHub icon button to fetch and display your latest repositories
- **Real-time Data**: Shows current info (stars, forks, languages, topics)
- **Language Filtering**: Users can filter projects by programming language
- **Topic Tags**: Displays topics/tags for each repository
- **README Included**: Links directly to GitHub for full README viewing
- **Beautiful Modal**: Projects displayed in a sleek modal interface with sorting options

### 📋 What Gets Displayed
For each repository:
- Repository name with link to GitHub
- Description
- Programming language with color coding
- Stars and forks count
- Topics/tags
- Direct GitHub link

### 🎯 User Experience
1. User sees a **GitHub icon button** next to the search bar
2. Clicks it to open the projects modal
3. Sees all repositories with filtering options
4. Can filter by programming language
5. Can click any project to view it on GitHub

## Setup Instructions

### Step 1: Generate GitHub Personal Access Token (Optional but Recommended)

The GitHub integration works **without a token**, but has rate limits. Adding a token increases your rate limit significantly.

#### Option A: With Personal Access Token (Recommended)

1. Go to [GitHub Settings → Personal Access Tokens](https://github.com/settings/tokens)
   - Or navigate: GitHub → Settings (top right) → Developer settings → Personal access tokens

2. Click **"Generate new token"** (classic token)

3. Configure the token:
   - **Token name**: `portfolio-chatbot` (or any name you prefer)
   - **Expiration**: Choose 90 days or 1 year
   - **Scopes needed**: Only check `public_repo` (read-only access to public repositories)
   
   > **Note**: You ONLY need `public_repo` scope. Do NOT select `repo` (full access).

4. Click **"Generate token"**

5. **COPY THE TOKEN IMMEDIATELY** ⚠️ 
   - You won't be able to see it again after leaving this page
   - If you lose it, regenerate a new one

#### Option B: Without Token (No Setup Required)

The integration works without a token, but with rate limiting (~60 requests/hour).

### Step 2: Configure in Your Backend (If Using Token)

Only do this if you have a token from Step 1.

1. Create or edit `.env` file in `backend/` directory:

```bash
# backend/.env
OPENROUTER_API_KEY=your_existing_key_here
GITHUB_TOKEN=your_github_token_here
```

**Example:**
```
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxx
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

2. Save the file

### Step 3: Restart Backend

Restart your backend server:

```bash
# Stop the current server (Ctrl+C)
# Then restart:
cd backend
python main.py
```

You should see:
```
✅ GitHub integration initialized
```

If you see a warning about GitHub not being available, that's fine - it still works without a token.

## Using the Feature

### In the Chat Interface

1. **Look for the GitHub icon button** next to the search bar (left side of input field)
   - Icon: ![github icon]
   - Hover shows tooltip: "View GitHub Projects"

2. **Click the GitHub button** to open the Projects Modal

3. **Browse your repositories**:
   - See all your repositories with descriptions
   - View star counts and fork counts
   - See programming languages used
   - View topics/tags for each project

4. **Filter by language** (if available):
   - Click language buttons to filter
   - Shows count of projects in each language
   - "All" button shows all projects

5. **Click any project** to visit it on GitHub in a new tab

### Testing the Integration

#### In Browser

1. **Open Developer Console** (F12)
2. Try fetching repositories directly:
   ```
   http://localhost:8000/github/repositories
   ```
3. Should see JSON with all your repositories

#### In Chat

1. Click the **GitHub icon button** next to search bar
2. Modal should open and load your repositories
3. Filter by language to test filtering
4. Click a project to visit GitHub

## Troubleshooting

### ❌ Button doesn't appear or modal won't open

**Solution**: 
- Ensure backend is running
- Check browser console for errors (F12)
- Restart backend server
- Clear browser cache and refresh

### ❌ "Failed to load projects" error

**Solution**: 
- Backend server might be down - restart it
- Check that GitHub API is accessible
- Try adding a GitHub token (see Setup Step 1)
- Check backend logs for detailed errors

### ❌ Very slow loading or frequent timeouts

**Solution**:
- Add a GitHub personal access token (increases speed and reliability)
- See Step 1 above for token generation

### ❌ Rate limit reached without token

**Solution**:
- Generate and add a GitHub token (see Step 1)
- With token: ~5,000 requests/hour
- Reset time: 1 hour after hitting limit

### ❌ Private repositories don't show up

**Solution**: 
- Only public repositories are displayed (by design for security)
- If you want to include private repos, update token scope in GitHub settings

## Advanced Configuration

### Change GitHub Username

To show repositories from a different GitHub account:

1. Edit `backend/config.py`
2. Find `GITHUB_CONFIG`
3. Update `"username"` field:

```python
GITHUB_CONFIG = {
    "username": "different-username",  # Change this
    # ... rest of config
}
```

4. Restart backend

### API Rate Limiting

- **Without Token**: ~60 requests/hour
- **With Token**: ~5,000 requests/hour per GitHub account
- **Rate limit window**: 1 hour from first request

Add a token to avoid hitting rate limits!

## Next Steps

1. ✅ (Optional) Generate GitHub token for better rate limits
2. ✅ (Optional) Add GITHUB_TOKEN to `.env` file  
3. ✅ Restart backend
4. ✅ Look for GitHub icon button next to search bar in chat
5. ✅ Click it to view your projects!

## Summary

- **GitHub button** is now a feature in the chat interface
- Click to see all your public repositories
- Filter by programming language
- No automatic fetching - completely opt-in
- Works best with a personal access token
- Token is optional but recommended for reliability

---

**Questions or Issues?** Check the backend console logs (where you started `python main.py`) for detailed error messages.
