# Discord Bot Runner - GitHub Actions

This repository contains Discord bots that automatically send messages to Discord threads every 5 minutes using GitHub Actions.

## ⚠️ Important Warning

**Using user tokens for automation violates Discord's Terms of Service. This code is for educational purposes only!**

## 🚀 Setup Instructions

### 1. Fork this Repository

1. Click the "Fork" button in the top-right corner of this repository
2. Clone your forked repository to your local machine

### 2. Configure GitHub Secrets

You need to set up GitHub Secrets to store your Discord tokens and thread IDs securely.

#### Required Secrets:

- `USER_TOKEN_C` - Discord user token for Bot C
- `THREAD_ID_C` - Discord thread ID for Bot C  
- `USER_TOKEN_D` - Discord user token for Bot D
- `THREAD_ID_D` - Discord thread ID for Bot D

#### To add secrets:

1. Go to your forked repository on GitHub
2. Click on **Settings** tab
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. Add each secret with the appropriate name and value

### 3. Get Your Discord User Token

1. Open Discord in your web browser (not the app)
2. Press `F12` to open Developer Tools
3. Go to the **Network** tab
4. Send a message in any Discord channel
5. Look for a request named `messages` in the Network tab
6. Click on it and find the **Request Headers**
7. Copy the value of the `Authorization` header (this is your user token)

### 4. Get Your Discord Thread ID

1. In Discord, enable **Developer Mode**:
   - Go to User Settings (gear icon)
   - Go to **Advanced** 
   - Turn on **Developer Mode**
2. Right-click on the thread you want to send messages to
3. Select **Copy Thread ID**

### 5. Set Up the Secrets

Add the following secrets to your GitHub repository:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `USER_TOKEN_C` | Your Discord user token for Bot C | `MTI2NjY5NDgwNzUxOTIzNjEwNw.GCwVG-...` |
| `THREAD_ID_C` | Discord thread ID for Bot C | `1381995998263513221` |
| `USER_TOKEN_D` | Your Discord user token for Bot D | `MTI2NjY5NDgwNzUxOTIzNjEwNw.GCwVG-...` |
| `THREAD_ID_D` | Discord thread ID for Bot D | `1399139526089113692` |

## 🔄 How It Works

- **Schedule**: The bots run automatically every 5 minutes using GitHub Actions cron schedule
- **Execution**: Each bot sends one message per run to its configured Discord thread
- **Logging**: All activity is logged and stored as artifacts for 7 days
- **Error Handling**: If a bot fails, the workflow continues with the other bot

## 📁 File Structure

```
.
├── .github/
│   └── workflows/
│       └── discord-bot.yml    # GitHub Actions workflow
├── c.py                       # Discord Bot C
├── d.py                       # Discord Bot D
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## 🛠️ GitHub Actions Workflow

The workflow (`discord-bot.yml`) includes:

- **Trigger**: Runs every 5 minutes (`*/5 * * * *`)
- **Manual Trigger**: Can be run manually via GitHub Actions UI
- **Python Setup**: Uses Python 3.11
- **Dependencies**: Installs requirements from `requirements.txt`
- **Bot Execution**: Runs both bots with their respective environment variables
- **Error Handling**: Continues execution even if one bot fails
- **Logging**: Uploads log files as artifacts

## 🔧 Customization

### Modify Messages

Edit the `CUSTOM_MESSAGES` list in either `c.py` or `d.py`:

```python
CUSTOM_MESSAGES = [
    "Your custom message 1",
    "Your custom message 2",
    "Another message with emoji 🎉"
]
```

### Change Schedule

Modify the cron schedule in `.github/workflows/discord-bot.yml`:

```yaml
schedule:
  - cron: '*/5 * * * *'  # Every 5 minutes
  # - cron: '*/10 * * * *'  # Every 10 minutes
  # - cron: '0 * * * *'     # Every hour
```

### Add More Bots

1. Create a new Python file (e.g., `e.py`)
2. Add corresponding secrets (`USER_TOKEN_E`, `THREAD_ID_E`)
3. Add a new step in the GitHub Actions workflow

## 📊 Monitoring

### View Logs

1. Go to **Actions** tab in your GitHub repository
2. Click on a workflow run
3. View the logs for each bot step
4. Download log artifacts if needed

### Check Status

- Green checkmark ✅: Bot ran successfully
- Red X ❌: Bot encountered an error
- Yellow circle 🟡: Bot is currently running

## 🚨 Troubleshooting

### Common Issues:

1. **Invalid Token**: Make sure your Discord user token is correct and hasn't expired
2. **Invalid Thread ID**: Verify the thread ID is correct and the bot has access
3. **Rate Limiting**: Discord may rate limit requests; the bot will handle this automatically
4. **Permissions**: Ensure the user account has permission to send messages in the thread

### Debug Steps:

1. Check the GitHub Actions logs for error messages
2. Verify all secrets are set correctly
3. Test locally by setting environment variables
4. Ensure Discord Developer Mode is enabled

## 📝 Local Testing

To test locally:

1. Set environment variables:
   ```bash
   export USER_TOKEN_C="your_token_here"
   export THREAD_ID_C="your_thread_id_here"
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the bot:
   ```bash
   python c.py
   ```

## 🔒 Security Notes

- Never commit your Discord tokens to the repository
- Use GitHub Secrets for all sensitive information
- The fallback tokens in the code should be removed for production use
- Monitor your bot's activity to ensure it's not being misused

## 📄 License

This project is for educational purposes only. Use at your own risk and in compliance with Discord's Terms of Service.