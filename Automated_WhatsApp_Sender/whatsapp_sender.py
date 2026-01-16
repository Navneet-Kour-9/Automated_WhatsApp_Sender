"""
WhatsApp Message Sender - Main Module
Author: Navneet Kour
Description: Automated WhatsApp messaging using PyWhatKit
"""

import pywhatkit as kit
import pandas as pd
from datetime import datetime
import time
from colorama import init, Fore, Style
import config

# Initialize colorama for colored output
init()


def send_message(phone_number: str, message: str, wait_time: int = None) -> bool:
    """
    Send a WhatsApp message to a single contact.
    
    Args:
        phone_number: Phone number with country code (e.g., +91XXXXXXXXXX)
        message: Message to send
        wait_time: Time to wait for WhatsApp Web to load (optional)
        
    Returns:
        bool: True if message sent successfully, False otherwise
    """
    if wait_time is None:
        wait_time = config.WAIT_TIME
    
    try:
        # Ensure phone number has country code
        if not phone_number.startswith('+'):
            phone_number = config.DEFAULT_COUNTRY_CODE + phone_number
        
        print(f"{Fore.CYAN}📤 Sending message to {phone_number}...{Style.RESET_ALL}")
        
        # Get current time and add 2 minutes
        now = datetime.now()
        hour = now.hour
        minute = now.minute + 2
        
        if minute >= 60:
            hour += 1
            minute -= 60
        
        # Send the message
        kit.sendwhatmsg(
            phone_number, 
            message, 
            hour, 
            minute, 
            wait_time=wait_time,
            tab_close=True,
            close_time=config.CLOSE_TIME
        )
        
        print(f"{Fore.GREEN}✅ Message sent successfully to {phone_number}!{Style.RESET_ALL}")
        log_message(phone_number, message, "SUCCESS")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ Failed to send message to {phone_number}: {str(e)}{Style.RESET_ALL}")
        log_message(phone_number, message, f"FAILED: {str(e)}")
        return False


def send_instant_message(phone_number: str, message: str) -> bool:
    """
    Send an instant WhatsApp message (opens WhatsApp Web immediately).
    
    Args:
        phone_number: Phone number with country code
        message: Message to send
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if not phone_number.startswith('+'):
            phone_number = config.DEFAULT_COUNTRY_CODE + phone_number
            
        print(f"{Fore.CYAN}⚡ Sending instant message to {phone_number}...{Style.RESET_ALL}")
        
        kit.sendwhatmsg_instantly(
            phone_number,
            message,
            wait_time=config.WAIT_TIME,
            tab_close=True,
            close_time=config.CLOSE_TIME
        )
        
        print(f"{Fore.GREEN}✅ Instant message sent to {phone_number}!{Style.RESET_ALL}")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ Failed: {str(e)}{Style.RESET_ALL}")
        return False


def send_bulk_messages(contacts_file: str, message: str, personalize: bool = False) -> dict:
    """
    Send messages to multiple contacts from a CSV file.
    
    Args:
        contacts_file: Path to CSV file with 'name' and 'phone' columns
        message: Message to send (use {name} for personalization)
        personalize: Whether to personalize message with contact name
        
    Returns:
        dict: Results with success and failure counts
    """
    results = {"success": 0, "failed": 0, "details": []}
    
    try:
        # Load contacts from CSV
        df = pd.read_csv(contacts_file)
        total = len(df)
        
        print(f"{Fore.YELLOW}📋 Loaded {total} contacts from {contacts_file}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'='*50}{Style.RESET_ALL}")
        
        for index, row in df.iterrows():
            name = row.get('name', 'Friend')
            phone = str(row['phone'])
            
            # Personalize message if enabled
            current_message = message.replace("{name}", name) if personalize else message
            
            print(f"\n{Fore.CYAN}[{index + 1}/{total}] Processing: {name}{Style.RESET_ALL}")
            
            success = send_message(phone, current_message)
            
            if success:
                results["success"] += 1
            else:
                results["failed"] += 1
            
            results["details"].append({
                "name": name,
                "phone": phone,
                "status": "success" if success else "failed"
            })
            
            # Wait between messages to avoid rate limiting
            if index < total - 1:
                print(f"{Fore.YELLOW}⏳ Waiting 30 seconds before next message...{Style.RESET_ALL}")
                time.sleep(30)
        
        print(f"\n{Fore.GREEN}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}📊 BULK SEND COMPLETE{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✅ Successful: {results['success']}{Style.RESET_ALL}")
        print(f"{Fore.RED}❌ Failed: {results['failed']}{Style.RESET_ALL}")
        
        return results
        
    except Exception as e:
        print(f"{Fore.RED}❌ Error in bulk send: {str(e)}{Style.RESET_ALL}")
        return results


def log_message(phone: str, message: str, status: str):
    """Log message details to a file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {phone} | {status} | {message[:50]}...\n"
    
    with open(config.LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry)


def main():
    """Main function to demonstrate usage."""
    print(f"{Fore.CYAN}")
    print("=" * 50)
    print("   📱 WhatsApp Automated Sender")
    print("   By: Navneet Kour")
    print("=" * 50)
    print(f"{Style.RESET_ALL}")
    
    print("\nOptions:")
    print("1. Send single message")
    print("2. Send bulk messages")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        phone = input("Enter phone number (with country code): ").strip()
        message = input("Enter your message: ").strip()
        send_message(phone, message)
        
    elif choice == "2":
        file_path = input("Enter CSV file path (default: contacts.csv): ").strip()
        if not file_path:
            file_path = config.CONTACTS_FILE
        message = input("Enter your message (use {name} for personalization): ").strip()
        personalize = input("Personalize messages? (y/n): ").lower() == 'y'
        send_bulk_messages(file_path, message, personalize)
        
    else:
        print(f"{Fore.YELLOW}👋 Goodbye!{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
