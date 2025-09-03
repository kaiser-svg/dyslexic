"""
Discord Thread Message Bot
A Python bot that automatically sends messages to a Discord thread using user tokens.

WARNING: Using user tokens for automation violates Discord's Terms of Service.
This code is for educational purposes only!

Author: Assistant
Version: 2.0
"""

import requests
import time
import json
import random
import logging
import os
import sys
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class BotConfig:
    """Configuration class for the Discord bot."""
    user_token: str
    thread_id: str
    interval: int = 60  # seconds
    messages: Optional[List[str]] = None
    
    def __post_init__(self):
        """Set default messages if none provided."""
        if self.messages is None:
            self.messages = [
                "Automated message from Python bot! 🐍",
                "Bot check-in #{} 🤖",
                "Still monitoring this thread! 👀",
                "Regular automated update 📡",
                "Python bot is alive and well! ✨",
                "Keeping the thread active! 🔄",
                "Status report: All systems operational ✅",
                "Hello from the automated messenger! 👋"
            ]


class DiscordAPI:
    """Handle Discord API interactions."""
    
    BASE_URL = "https://discord.com/api/v9"
    
    def __init__(self, token: str):
        self.token = token
        self.session = requests.Session()
        self.session.headers.update(self._get_headers())
        
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for Discord API requests."""
        return {
            "Authorization": self.token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIwLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjI1ODc0MywiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0="
        }
    
    def get_channel_info(self, channel_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a channel/thread."""
        try:
            url = f"{self.BASE_URL}/channels/{channel_id}"
            response = self.session.get(url)
            
            if response.status_code == 200:
                return response.json()
            else:
                logging.error(f"Failed to get channel info. Status: {response.status_code}, Response: {response.text}")
                return None
                
        except Exception as e:
            logging.error(f"Error getting channel info: {str(e)}")
            return None
    
    def send_message(self, channel_id: str, content: str) -> bool:
        """Send a message to a channel/thread."""
        try:
            url = f"{self.BASE_URL}/channels/{channel_id}/messages"
            payload = {"content": content}
            
            response = self.session.post(url, json=payload)
            
            if response.status_code == 200:
                return True
            elif response.status_code == 429:
                # Handle rate limiting
                retry_after = response.json().get('retry_after', 60)
                logging.warning(f"Rate limited. Waiting {retry_after} seconds...")
                time.sleep(retry_after)
                return False
            else:
                logging.error(f"Failed to send message. Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            logging.error(f"Error sending message: {str(e)}")
            return False


class MessageGenerator:
    """Generate messages for the bot to send."""
    
    def __init__(self, messages: List[str]):
        self.messages = messages
        self.message_count = 0
    
    def get_next_message(self) -> str:
        """Get the next message to send."""
        self.message_count += 1
        
        # Select a random message
        message_template = random.choice(self.messages)
        
        # Format with counter if placeholder exists
        if "{}" in message_template:
            return message_template.format(self.message_count)
        
        return message_template
    
    def get_message_count(self) -> int:
        """Get the total number of messages sent."""
        return self.message_count


class DiscordThreadBot:
    """Main bot class that orchestrates the messaging."""
    
    def __init__(self, config: BotConfig):
        self.config = config
        self.api = DiscordAPI(config.user_token)
        self.message_generator = MessageGenerator(config.messages)
        self.running = False
        
        # Setup logging
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration."""
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('logs/discord_bot_c.log')
            ]
        )
    
    def validate_config(self) -> bool:
        """Validate the bot configuration."""
        if not self.config.user_token or self.config.user_token == "YOUR_USER_TOKEN_HERE":
            logging.error("User token not configured!")
            return False
            
        if not self.config.thread_id or self.config.thread_id in ["YOUR_THREAD_ID_HERE", "PASTE_YOUR_THREAD_ID_HERE"]:
            logging.error("Thread ID not configured!")
            return False
            
        return True
    
    def test_connection(self) -> bool:
        """Test connection to Discord and thread access."""
        logging.info("Testing connection to Discord...")
        
        thread_info = self.api.get_channel_info(self.config.thread_id)
        
        if thread_info:
            thread_name = thread_info.get('name', 'Unknown Thread')
            guild_id = thread_info.get('guild_id', 'Unknown Server')
            logging.info(f"✅ Connected to thread: {thread_name} (Guild: {guild_id})")
            return True
        else:
            logging.error("❌ Cannot access thread. Check your token and thread ID.")
            return False
    
    def start(self):
        """Start the bot messaging loop."""
        self.running = True
        
        # Display startup information
        self._display_startup_info()
        
        # Validate configuration
        if not self.validate_config():
            self._display_config_help()
            return
        
        # Test connection
        if not self.test_connection():
            return
        
        # Start messaging loop
        logging.info("🚀 Starting message loop...")
        self._message_loop()
    
    def stop(self):
        """Stop the bot."""
        self.running = False
        logging.info("🛑 Bot stopped")
    
    def _display_startup_info(self):
        """Display startup information."""
        logging.info("🤖 Discord Thread Message Bot v2.0 (Bot C)")
        logging.info("=" * 50)
        logging.info("⚠️  WARNING: Using user tokens for automation violates Discord ToS")
        logging.info("📚 This is for educational purposes only!")
        logging.info("=" * 50)
        logging.info(f"📝 Thread ID: {self.config.thread_id}")
        logging.info(f"⏰ Message Interval: {self.config.interval} seconds")
        logging.info(f"📊 Available Messages: {len(self.config.messages)}")
        logging.info("=" * 50)
    
    def _display_config_help(self):
        """Display configuration help."""
        logging.error("❌ Configuration Error!")
        logging.error("\n🔧 How to configure:")
        logging.error("1. Set GitHub Secrets:")
        logging.error("   • USER_TOKEN_C: Your Discord user token")
        logging.error("   • THREAD_ID_C: Your Discord thread ID")
        logging.error("\n2. Get your user token:")
        logging.error("   • Open Discord in browser")
        logging.error("   • Press F12 → Network tab")
        logging.error("   • Send a message")
        logging.error("   • Look for 'messages' request")
        logging.error("   • Copy Authorization header")
        logging.error("\n3. Get your thread ID:")
        logging.error("   • Right-click on thread")
        logging.error("   • Select 'Copy Thread ID'")
        logging.error("   • (Enable Developer Mode in Discord settings if needed)")
    
    def _message_loop(self):
        """Main messaging loop optimized for GitHub Actions."""
        try:
            # For GitHub Actions: send one message and exit
            # The workflow will run again in 5 minutes
            message = self.message_generator.get_next_message()
            success = self.api.send_message(self.config.thread_id, message)
            
            if success:
                logging.info(f"✅ Message sent: {message[:50]}...")
                logging.info(f"📊 Total messages sent: {self.message_generator.get_message_count()}")
                logging.info("🎯 GitHub Actions run completed successfully")
            else:
                logging.warning("❌ Failed to send message")
                sys.exit(1)  # Exit with error code for GitHub Actions
                
        except KeyboardInterrupt:
            logging.info("🛑 Bot stopped by user (Ctrl+C)")
        except Exception as e:
            logging.error(f"❌ Unexpected error: {str(e)}")
            sys.exit(1)  # Exit with error code for GitHub Actions
        finally:
            self.stop()


def create_custom_config() -> BotConfig:
    """Create a custom bot configuration using environment variables."""
    
    # Get configuration from environment variables (GitHub Secrets)
    USER_TOKEN = os.getenv('USER_TOKEN_C')
    THREAD_ID = os.getenv('THREAD_ID_C')
    
    # Validate required environment variables
    if not USER_TOKEN:
        logging.error("USER_TOKEN_C environment variable is required!")
        logging.error("Set this in GitHub Secrets for the repository.")
        sys.exit(1)
    
    if not THREAD_ID:
        logging.error("THREAD_ID_C environment variable is required!")
        logging.error("Set this in GitHub Secrets for the repository.")
        sys.exit(1)
    
    # Message interval optimized for GitHub Actions (5 minutes = 300 seconds)
    # Since GitHub Actions runs every 5 minutes, we'll send one message per run
    INTERVAL = 1  # Just 1 second, then exit
    
    # Custom messages (optional)
    CUSTOM_MESSAGES = [
        "sigma :p",
        "peps.",
        "happy :D",
        "pfft spotted📡",
        "sparkle sparkle little twinkle✨",
        "repeating sir🔄",
        "check like a boss✅",
        "hello people👋!"
    ]
    
    return BotConfig(
        user_token=USER_TOKEN,
        thread_id=THREAD_ID,
        interval=INTERVAL,
        messages=CUSTOM_MESSAGES
    )


def main():
    """Main entry point."""
    try:
        # Create bot configuration
        config = create_custom_config()
        
        # Create and start bot
        bot = DiscordThreadBot(config)
        bot.start()
        
    except Exception as e:
        logging.error(f"Failed to start bot: {str(e)}")


if __name__ == "__main__":
    main()