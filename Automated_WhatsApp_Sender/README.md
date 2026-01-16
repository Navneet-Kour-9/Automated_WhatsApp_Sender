# 📱 Automated WhatsApp Sender

A Python-based automation tool for sending bulk WhatsApp messages. This tool integrates with WhatsApp Web to send scheduled messages, reducing manual effort by 80%.

## ✨ Features

- 📤 Send bulk messages to multiple contacts
- ⏰ Schedule messages for specific times
- 📁 Import contacts from CSV/Excel files
- 📝 Message templates with personalization
- 📊 Delivery status tracking
- 🔄 Automatic retry for failed messages

## 🛠️ Technologies Used

- Python 3.x
- PyWhatKit
- Pandas (for contact management)
- Openpyxl (for Excel support)
- Schedule (for scheduling)

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/Navneet-kour-9/Automated_WhatsApp_Sender.git

# Navigate to project directory
cd Automated_WhatsApp_Sender

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Usage

### Send a Single Message
```python
from whatsapp_sender import send_message

send_message("+91XXXXXXXXXX", "Hello! This is an automated message.")
```

### Send Bulk Messages
```python
from whatsapp_sender import send_bulk_messages

# Load contacts from CSV
send_bulk_messages("contacts.csv", "Your message here")
```

### Schedule a Message
```python
from whatsapp_sender import schedule_message

schedule_message("+91XXXXXXXXXX", "Good Morning!", hour=9, minute=0)
```

## 📁 Project Structure

```
Automated_WhatsApp_Sender/
├── whatsapp_sender.py      # Main sender module
├── scheduler.py            # Message scheduling
├── contact_manager.py      # Contact management
├── config.py              # Configuration settings
├── requirements.txt       # Dependencies
├── contacts_sample.csv    # Sample contacts file
└── README.md              # Documentation
```

## ⚠️ Disclaimer

This tool is for educational purposes only. Please use responsibly and in accordance with WhatsApp's Terms of Service.

## 👤 Author

**Navneet Kour**
- GitHub: [@Navneet-kour-9](https://github.com/Navneet-kour-9)
- Email: Udayjots516@gmail.com

## 📄 License

This project is licensed under the MIT License.
