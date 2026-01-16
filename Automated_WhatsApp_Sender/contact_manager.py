"""
Contact Manager Module
Author: Navneet Kour
Description: Manage contacts for bulk messaging
"""

import pandas as pd
from colorama import init, Fore, Style
import os

init()


class ContactManager:
    """Manage contacts for WhatsApp messaging."""
    
    def __init__(self, file_path: str = "contacts.csv"):
        self.file_path = file_path
        self.contacts = self._load_contacts()
    
    def _load_contacts(self) -> pd.DataFrame:
        """Load contacts from CSV file."""
        if os.path.exists(self.file_path):
            return pd.read_csv(self.file_path)
        else:
            # Create empty DataFrame with required columns
            return pd.DataFrame(columns=['name', 'phone', 'group'])
    
    def save_contacts(self):
        """Save contacts to CSV file."""
        self.contacts.to_csv(self.file_path, index=False)
        print(f"{Fore.GREEN}✅ Contacts saved to {self.file_path}{Style.RESET_ALL}")
    
    def add_contact(self, name: str, phone: str, group: str = "general"):
        """Add a new contact."""
        new_contact = pd.DataFrame([{
            'name': name,
            'phone': phone,
            'group': group
        }])
        self.contacts = pd.concat([self.contacts, new_contact], ignore_index=True)
        self.save_contacts()
        print(f"{Fore.GREEN}✅ Added contact: {name}{Style.RESET_ALL}")
    
    def remove_contact(self, phone: str):
        """Remove a contact by phone number."""
        initial_count = len(self.contacts)
        self.contacts = self.contacts[self.contacts['phone'] != phone]
        
        if len(self.contacts) < initial_count:
            self.save_contacts()
            print(f"{Fore.GREEN}✅ Contact removed{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠️ Contact not found{Style.RESET_ALL}")
    
    def list_contacts(self, group: str = None):
        """List all contacts or filter by group."""
        contacts = self.contacts
        
        if group:
            contacts = contacts[contacts['group'] == group]
        
        if len(contacts) == 0:
            print(f"{Fore.YELLOW}📋 No contacts found{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📋 CONTACTS LIST{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        
        for idx, row in contacts.iterrows():
            print(f"{idx + 1}. {row['name']} | {row['phone']} | [{row['group']}]")
        
        print(f"\n{Fore.GREEN}Total: {len(contacts)} contacts{Style.RESET_ALL}")
    
    def get_contacts_by_group(self, group: str) -> list:
        """Get phone numbers by group."""
        filtered = self.contacts[self.contacts['group'] == group]
        return filtered['phone'].tolist()
    
    def import_from_excel(self, excel_path: str):
        """Import contacts from Excel file."""
        try:
            df = pd.read_excel(excel_path)
            self.contacts = pd.concat([self.contacts, df], ignore_index=True)
            self.contacts.drop_duplicates(subset=['phone'], keep='last', inplace=True)
            self.save_contacts()
            print(f"{Fore.GREEN}✅ Imported {len(df)} contacts from Excel{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ Import failed: {str(e)}{Style.RESET_ALL}")
    
    def export_to_excel(self, excel_path: str = "contacts_export.xlsx"):
        """Export contacts to Excel file."""
        try:
            self.contacts.to_excel(excel_path, index=False)
            print(f"{Fore.GREEN}✅ Exported to {excel_path}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ Export failed: {str(e)}{Style.RESET_ALL}")


def main():
    """Interactive contact management."""
    manager = ContactManager()
    
    while True:
        print(f"\n{Fore.CYAN}📱 Contact Manager{Style.RESET_ALL}")
        print("1. List contacts")
        print("2. Add contact")
        print("3. Remove contact")
        print("4. Import from Excel")
        print("5. Export to Excel")
        print("6. Exit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            manager.list_contacts()
        elif choice == "2":
            name = input("Name: ").strip()
            phone = input("Phone: ").strip()
            group = input("Group (default: general): ").strip() or "general"
            manager.add_contact(name, phone, group)
        elif choice == "3":
            phone = input("Phone to remove: ").strip()
            manager.remove_contact(phone)
        elif choice == "4":
            path = input("Excel file path: ").strip()
            manager.import_from_excel(path)
        elif choice == "5":
            manager.export_to_excel()
        elif choice == "6":
            print(f"{Fore.YELLOW}👋 Goodbye!{Style.RESET_ALL}")
            break


if __name__ == "__main__":
    main()
