# Crypture - Image Encryption and Decryption Tool

Crypture is a desktop application that allows users to securely encrypt and decrypt image files using AES (Advanced Encryption Standard). It features a simple and modern graphical interface, making the process easy for both technical and non-technical users.

## Features

- AES-based encryption using EAX mode for confidentiality and integrity.
- Supports `.jpg`, `.jpeg`, and `.png` image formats.
- Dynamically determines key size based on file size for optimized security.
- Option to save encrypted files locally or send them directly via email.
- Intuitive CustomTkinter-based GUI with dark theme.
- Decryption requires the correct key, ensuring that data remains protected.

## How it Works

### Encryption

1. Choose one or more image files.
2. Based on the size of the image(s), a required key length is determined:
   - Less than 2MB → 32-byte key (15-character input)
   - Between 2MB and 10MB → 24-byte key (11-character input)
   - More than 10MB → 16-byte key (7-character input)
3. Enter your custom key and encrypt the file(s).
4. Save the output locally or send it as an email attachment.

### Decryption

1. Choose encrypted `.bin` files.
2. Provide the original key used during encryption.
3. If the key is correct, the image(s) will be restored to their original form.

## Technologies Used

- Python 3.x
- CustomTkinter (for GUI)
- PyCryptodome (AES encryption/decryption)
- Pillow (Image processing)
- smtplib and email (for email functionality)

## Installation

### Prerequisites

- Python 3.8 or above installed

### Steps

```bash
git clone https://github.com/yourusername/crypture.git
cd crypture
pip install -r requirements.txt
python crypture.py
