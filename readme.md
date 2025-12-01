# 📚 DSA Learning Platform — Flask + MongoDB + Vercel

A modern and responsive web application built using **Flask**, **MongoDB**, and **Vercel**, designed to help users learn **Data Structures and Algorithms (DSA)** topic-wise.  
The platform includes **authentication**, **admin panel**, **glassmorphism UI**, and **email-based password reset (OTP or link-based)**.

---

## 🚀 Short Description

This project is a full-stack web application where users can register, log in, and explore DSA topics such as **Searching Algorithms**, **Linked Lists**, **Trees**, **Graphs**, **Recursion**, and more.  
Admin users can add new topics dynamically.  
The UI is clean, minimal, and uses **glassmorphism** for modern aesthetics.  
Password reset is handled through **SMTP email** using OTP or secure token links.

---

## ✨ Features

### 🔐 Authentication System
- User Registration  
- Login  
- Logout  
- Forgot Password (OTP or token link)  
- Secure password hashing with Werkzeug  

### 📘 DSA Learning Module
- Topic-wise pages (Searching, Sorting, Trees, Graphs, Recursion, etc.)  
- Each topic has explanations + Python code examples  
- Visual and clean layouts  

### 🛠 Admin Panel
- Add / Edit / Delete DSA topics  
- Accessible only to admin users  

### 🎨 UI & Styling
- Fully responsive  
- Glassmorphism design  
- Clean & modern templates  

### 📬 Email Support
- SMTP integration using Flask-Mail  
- Works with Gmail, Outlook, Zoho, SendGrid  
- Sends OTP or reset links  

### ☁ Deployment Ready
- Structured to deploy on **Vercel (Serverless Python)**  
- Includes `requirements.txt` and optional `vercel.json`  

---

## 📁 Project Structure
project/
│── app.py
│── requirements.txt
│── vercel.json (optional for link routes)
│── templates/
│ ├── base.html
│ ├── index.html
│ ├── login.html
│ ├── register.html
│ ├── forgot.html
│ ├── verify_otp.html
│ ├── reset_password.html
│ ├── dashboard.html
│ ├── topic_detail.html
│ └── admin.html
│── static/
├── css/
│ └── style.css
└── js/
└── script.js


---

## 🔧 Installation (Local Setup)

### 1️⃣ Clone the repository
```bash
git clone https://github.com/FairozAhmadSheikh/learn_dsa_easy_way_using_python
cd learn_dsa_easy_way_using_python
```
###  Create a virtual environment

python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies

pip install -r requirements.txt

### Set environment variables

Create .env file:
MONGO_URI=your_mongodb_connection_string
SECRET_KEY=your_secret_key
SMTP_EMAIL=your_email
SMTP_PASSWORD=your_app_password

### 🤝 Contributing

Pull requests are welcome!
If you want to add new DSA topics or improve UI, feel free to contribute.

### 📄 License

This project is open-source and available under the MIT License.

### ❤️ Acknowledgements

    Built using:

    Flask

    MongoDB

    Flask-Mail

    Jinja2

    Python

    Vercel

Designed with love for learners exploring DSA.