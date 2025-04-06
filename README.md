# Digital-Signature-Scheme
A secure, web-based application that implements the Digital Signature Standard (DSS) using Elliptic Curve Cryptography (ECDSA). This project demonstrates a real-world cryptographic system for message signing, verification, and key management, tailored with a modern and interactive user interface.

---

## 📌 Features

- **Key Pair Generation** (ECDSA with SECP256R1 curve)
- **Digital Signing** of user-input messages
- **Signature Verification**
- **Signing History** with timestamps
- **User Authentication** (Sign up & login)
- JSON-based lightweight storage (no DB needed)
- Glassmorphism + Cyberpunk themed UI

---

## 🔧Technologies Used

### Backend
- Python 3
- Flask
- cryptography (Elliptic Curve Digital Signature Algorithm)
- Jinja2 templating
- werkzeug (for password hashing)

### Frontend
- HTML / CSS
- Javascript

---

## 🗂 Folder Structure
project/ │  
├── app.py   
├── ds_core.py    
├── users.json   
├── history.json      
├── /templates   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── login.html │   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── signup.html │   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── dashboard.html │  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── history.html │  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── index.html │  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── sign.html │  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── verify.html   
├── /static    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── dashboard.css │   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── style.css │   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── dashboard.js   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── /keys   

---

## 🚀 How to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```
2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask server:
   ```bash
   python app.py
   ```
4. Open in your browser:  
   http://localhost:5000
   
