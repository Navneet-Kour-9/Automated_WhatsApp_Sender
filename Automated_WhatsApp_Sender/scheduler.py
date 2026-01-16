"""
Message Scheduler Module
Author: Navneet Kour
Description: Schedule WhatsApp messages for specific times
"""

import pywhatkit as kit
import schedule
import time
from datetime import datetime
from colorama import init, Fore, Style
import config

init()


def schedule_message(phone_number: str, message: str, hour: int, minute: int) -> bool:
    """
    Schedule a WhatsApp message for a specific time.
    
    Args:
        phone_number: Phone number with country code
        message: Message to send
        hour: Hour (24-hour format)
        minute: Minute
        
    Returns:
        bool: True if scheduled successfully
    """
    try:
        if not phone_number.startswith('+'):
            phone_number = config.DEFAULT_COUNTRY_CODE + phone_number
        
        print(f"{Fore.CYAN}⏰ Scheduling message for {hour:02d}:{minute:02d}...{Style.RESET_ALL}")
        
        kit.sendwhatmsg(
            phone_number,
            message,
            hour,
            minute,
            wait_time=config.WAIT_TIME,
            tab_close=True
        )
        
        print(f"{Fore.GREEN}✅ Message scheduled successfully!{Style.RESET_ALL}")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ Failed to schedule: {str(e)}{Style.RESET_ALL}")
        return False


def schedule_daily_message(phone_number: str, message: str, time_str: str):
    """
    Schedule a daily recurring message.
    
    Args:
        phone_number: Phone number with country code
        message: Message to send
        time_str: Time in HH:MM format (24-hour)
    """
    def job():
        print(f"{Fore.YELLOW}🔔 Running scheduled job...{Style.RESET_ALL}")
        now = datetime.now()
        schedule_message(phone_number, message, now.hour, now.minute + 2)
    
    schedule.every().day.at(time_str).do(job)
    
    print(f"{Fore.GREEN}✅ Daily message scheduled for {time_str}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}⏳ Scheduler running... Press Ctrl+C to stop{Style.RESET_ALL}")
    
    while True:
        schedule.run_pending()
        time.sleep(60)


def schedule_weekly_message(phone_number: str, message: str, day: str, time_str: str):
    """
    Schedule a weekly recurring message.
    
    Args:
        phone_number: Phone number with country code
        message: Message to send
        day: Day of week (monday, tuesday, etc.)
        time_str: Time in HH:MM format
    """
    def job():
        now = datetime.now()
        schedule_message(phone_number, message, now.hour, now.minute + 2)
    
    # Get the correct day method
    day_method = getattr(schedule.every(), day.lower())
    day_method.at(time_str).do(job)
    
    print(f"{Fore.GREEN}✅ Weekly message scheduled for {day} at {time_str}{Style.RESET_ALL}")


if __name__ == "__main__":
    print(f"{Fore.CYAN}")
    print("=" * 50)
    print("   ⏰ WhatsApp Message Scheduler")
    print("   By: Navneet Kour")
    print("=" * 50)
    print(f"{Style.RESET_ALL}")
    
    phone = input("Enter phone number: ").strip()
    message = input("Enter message: ").strip()
    
    print("\nSchedule type:")
    print("1. One-time")
    print("2. Daily")
    
    choice = input("Enter choice: ").strip()
    
    if choice == "1":
        hour = int(input("Enter hour (24-hour format): "))
        minute = int(input("Enter minute: "))
        schedule_message(phone, message, hour, minute)
    else:
        time_str = input("Enter time (HH:MM): ")
        schedule_daily_message(phone, message, time_str)
