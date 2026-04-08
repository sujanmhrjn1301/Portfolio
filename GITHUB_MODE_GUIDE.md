# GitHub Mode - User Guide

## What is GitHub Mode?

**GitHub Mode** is like ChatGPT's Study Mode or Thinking Mode - an opt-in feature that enhances your chat experience for deep project discussions.

When you enable GitHub Mode:
- The AI automatically fetches your latest GitHub repository data
- You can ask detailed questions about your projects
- Responses include real-time information (stars, languages, topics, descriptions)
- Perfect for discussing projects, technologies, and code details

## How to Use GitHub Mode

### Enabling GitHub Mode

1. **Look for the "GitHub Mode" button** in the chat input area (left side, below the input field)
   
2. **Click the button** to enable GitHub Mode
   - Button changes color to blue when active
   - A green indicator shows "● Active"
   - Info banner appears at the top confirming it's enabled

3. **Ask detailed questions about projects:**
   - "Tell me about all your Python projects"
   - "What projects use React?"
   - "Which of your projects have the most stars?"
   - "Describe the architecture of my JavaScript projects"
   - "What are the most recent projects I've created?"

4. **Disable when done:**
   - Click the "GitHub Mode" button again to toggle it off
   - Or click "Turn Off" in the info banner

### Example Conversation Flow

**Normal Mode (Default):**
```
User: "What projects have you created?"
AI: [Responds with general projects from CV data]
```

**GitHub Mode:**
```
User: [Toggle GitHub Mode ON]
User: "What projects have you created?"
AI: [Fetches live GitHub data and responds with:
     - Project names, descriptions
     - Programming languages
     - Star counts
     - Recent activity
     - Topics/tags
     - Real-time repository information]
```

## Visual Indicators

### GitHub Mode Active:
- Button changes to blue background
- Green "● Active" indicator appears
- Info banner at top of input area explains mode is on
- Placeholder text changes to "Ask me anything about the projects..."

### GitHub Mode Inactive:
- Button remains grey
- No indicator badge
- Normal placeholder text
- Input area minimal

## Setup (Optional but Recommended)

GitHub Mode works **out of the box**, but for better performance:

1. Generate a GitHub Personal Access Token:
   - Go to https://github.com/settings/tokens
   - Create new token with `public_repo` scope
   - Copy the token

2. Add to `.env` in backend folder:
   ```
   GITHUB_TOKEN=ghp_your_token_here
   ```

3. Restart backend server

### Why Add a Token?

- **Without token**: ~60 API requests/hour
- **With token**: ~5,000 API requests/hour
- Better reliability for frequent mode usage

## What Data Gets Included

When GitHub Mode is enabled, the AI can access:

- **Repository Information:**
  - Name and full description
  - Programming languages used
  - Stars and forks count
  - Topics/tags
  - GitHub URLs
  - README content (when available)

- **Project Context:**
  - Real-time statistics
  - Latest activity
  - Technology stack
  - Code organization

## Tips for Best Results

1. **Be specific:** Instead of just "talk about projects", ask specific questions like:
   - "Which of my projects use Python?"
   - "What's the purpose of my most starred project?"
   - "Tell me about my web development projects"

2. **Deep dives:** GitHub Mode shines with detailed discussions:
   - "Compare my Python and JavaScript projects"
   - "Which projects would be good for a beginner to learn from?"
   - "What's the technology pattern in my recent projects?"

3. **Turn off when done:** Disable GitHub Mode when you're done with project discussions to reduce API usage

## Troubleshooting

### ❌ Button doesn't appear
- Refresh the browser
- Ensure frontend is running
- Check browser console for errors (F12)

### ❌ "Failed to load projects" error
- Backend server might be down
- Check that GitHub API is accessible
- Try adding a GitHub token (see Setup section)

### ❌ Mode toggles but doesn't work
- Restart backend server
- Check backend logs for errors
- Ensure `.env` file is properly configured (if using token)

### ❌ Slow responses in GitHub Mode
- This is normal - GitHub data is being fetched
- Add a token to improve speed (see Setup section)
- Wait a moment for the response

## Comparison

| Feature | Normal Mode | GitHub Mode |
|---------|-----------|-------------|
| **Performance** | Fast | Slightly slower (API call) |
| **Data Source** | CV database only | Live GitHub API data |
| **Best for** | General portfolio questions | Detailed project discussions |
| **API Usage** | None | 1 request per chat message |
| **Real-time Info** | No | Yes (latest repos, stars, etc.) |

## Examples

### Normal Mode
```
Q: "What projects have you created?"
A: [From CV data] "I have created several projects including..."
```

### GitHub Mode
```
Q: [Enable GitHub Mode]
Q: "What projects have you created?"
A: [With live GitHub data] "I've created 12 public repositories including:

🐍 Python Projects (5):
- project-name: Description... ⭐ 45 stars
- another-project: Description... ⭐ 12 stars
...

🟨 JavaScript Projects (4):
...

And more..."
```

## Notes

- GitHub Mode only shows **public repositories**
- For **private repositories**, update token scope in GitHub settings
- Mode state **resets** when you close/refresh the browser
- Enable it fresh in each session as needed
- No data is stored locally - it's fetched fresh each time

---

**Ready to go deep?** Enable GitHub Mode and start asking detailed questions about your projects! 🚀
