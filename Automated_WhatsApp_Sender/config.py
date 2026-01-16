"""
Configuration settings for WhatsApp Sender
"""

# Timing settings (in seconds)
WAIT_TIME = 15  # Time to wait for WhatsApp Web to load
CLOSE_TIME = 3  # Time to wait before closing the tab

# Message settings
DEFAULT_COUNTRY_CODE = "+91"
MAX_RETRY_ATTEMPTS = 3
RETRY_DELAY = 60  # seconds

# File paths
CONTACTS_FILE = "contacts.csv"
LOG_FILE = "message_log.txt"

# Scheduling defaults
DEFAULT_SCHEDULE_HOUR = 9
DEFAULT_SCHEDULE_MINUTE = 0
