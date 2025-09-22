# Mental Health Support & Education Chatbot
---
This project is part of my Final Year Project (FYP) at Universiti Teknikal Malaysia Melaka (UTeM). It focuses on developing a **Mental Health Support & Education Chatbot** that uses **Natural Language Processing (NLP)** and **Large Language Models (LLMs)** to provide accessible, confidential, and personalized mental health guidance. It allows users to interact at any time, helping to lower barriers such as limited access to services, high costs, or hesitation to seek professional help.

<br>

## Features

* **Suicide Risk Detection:** <br> NLP classifier trained on a custom dataset (7,500 entries) to detect suicidal vs. non-suicidal intent.

* **Conversational Chatbot:** <br> Integrated with the OpenAI GPT-3.5 API for context-aware, sensitive interactions.

* **Web Application (Flask):** <br> User-friendly interface with login, registration, and a landing page featuring mental health articles.

* **Admin Dashboard:** <br> Allows counselors/admins to monitor flagged high-risk cases.

* **Data Security:** <br> User data and chat logs are encrypted for confidentiality.

* **Cross-Platform Support:** <br> Responsive design for desktop and mobile users.

<br>

## Technologies Used
* **Programming Language:** Python

* **Frameworks & Libraries:**

  * Flask (web framework)
  
  * NLTK, scikit-learn (NLP & ML)
  
  * GPT-3.5 API (LLM for conversations)
  
  * Bootstrap, CSS (frontend styling)

* **Database:** SQLite with SQLAlchemy ORM

* **Development Tools:** Visual Studio Code, Google Colab

<br>

## Project Structure
```
mental-health-chatbot/
├── data/              # Mental health articles (Markdown format)
├── static/               # CSS, JavaScript, images, favicon
│   ├── css/
│   ├── js/
│   ├── images/
│   └── favicon.ico
├── instance/               # SQLite database files (user data, chat logs, predictions)
│   ├── db.sqlite           # Main database file
│   └── db_before_messages.sqlite  # Backup or test database
├── templates/            # HTML templates (base.html, index.html, login.html, etc.)
├── mental_health_app.py  # Main Flask app (includes routes, auth, chatbot, and classifier logic)
├── finalized_model.sav   # Trained scikit-learn model
├── requirements.txt      # Dependencies
├── suicide_detection.csv # Labeled text data (suicide vs. non-suicide)
└── README.md             # Documentation

```
<br>

## Installation & Setup

**1.** Clone this repository:
```
git clone https://github.com/yourusername/mental-health-chatbot.git
cd mental-health-chatbot
```
**2.** Create a virtual environment and install dependencies:
```
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
pip install -r requirements.txt
```
**3.** Set OpenAI API key:
* Open the ```mental_health_app.py``` file.

* Replace the placeholder with your actual OpenAI API key.

* **Important**: Without the API key, the program will still run and load the interface, but the chatbot will not generate replies.

**4.** Run the application:
```
python mental_health_app.py
```
**5.** Open your browser and go to:
```
http://127.0.0.1:5000/
```
<br>

## Model Performance

* **Classifier Accuracy**: ~89%

* **F1 Score**: ~88%

* **Suicide Detection Accuracy**: 98.3% (custom dataset)

<br>

## Security & Ethics

* All sensitive user data is encrypted.

* The **OpenAI API key must be kept private** - can not share it publicly (e.g., in GitHub repos).

* This chatbot is **not a replacement for professional therapy**.

* For critical cases, users are encouraged to seek immediate professional help.
 
> **Dataset Source**: The `suicide_detection.csv` file was downloaded from Kaggle under the dataset titled *"Suicide Detection"* by Faisal Ahmed (2021). Original Source: [https://www.kaggle.com/datasets/faisalahmed48/suicide-detection](https://www.kaggle.com/datasets/faisalahmed48/suicide-detection)   

<br>

## Future Enhancements

* Multilingual support for wider accessibility.

* Integration with real-time professional counseling.

* Mobile app version.

* Advanced conversation tracking and risk assessment features.

<br>

## Acknowledgements

This project was developed as part of my Final Year Project at **Universiti Teknikal Malaysia Melaka (UTeM)**.
Special thanks to my supervisor, peers, and everyone who supported me throughout this journey.

<br>

**Disclaimer**: This chatbot is a research prototype. It is intended for **educational purposes only** and should not be used as a substitute for professional mental health services.

<br>
