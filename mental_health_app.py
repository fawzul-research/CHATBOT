# for web app
from flask import Flask, render_template, request, url_for, redirect,abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user,login_required, current_user

import markdown
import os
# for large language model
from langchain import PromptTemplate, LLMChain

# from langchain.llms import GPT4All
from langchain.llms import OpenAI

# for classification model
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import HashingVectorizer
import numpy as np
import pickle
import re
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
nltk.download('stopwords')


clf = SGDClassifier(loss='log_loss', random_state=1)
clf = pickle.load(open('finalized_model.sav', 'rb'))
label = {0:'non-suicide', 1:'suicide'}

stop = stopwords.words('english')
porter = PorterStemmer()

def tokenizer_porter(text):
    return [porter.stem(word) for word in text.split()]

def tokenizer(text):
    text = re.sub('<[^>]*>', '', text)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\(|D|P)',text.lower())
    text = re.sub('[\W]+', ' ', text.lower())
    text += ' '.join(emoticons).replace('-', '')
    tokenized = [w for w in tokenizer_porter(text) if w not in stop]
    return tokenized

vect = HashingVectorizer(decode_error='ignore', n_features=2**21,
                         preprocessor=None,tokenizer=tokenizer)

system_message = """You are an AI mental health assistant. Your goal is to provide only valuable mental health advice to users.
User will you give you a question. Your task is to answer as faithfully as you can.
If the question is not related to mental health,tell the user that is not your domain and apologize kindly.
will pass to you the analysis of the user's message To help you generate a better response, DO NOT INCLUDE IT IN THE RESPONSE.
"""

template = """### System: {system_message}
### Analysis: {analysis}
### User: {user}
### Response: 
"""

prompt = PromptTemplate(template=template, input_variables=['user', 'analysis', 'system_message'])
llm = OpenAI(openai_api_key="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
# llm = GPT4All(model="orca-mini-3b.ggmlv3.q4_0.bin", temp=1, verbose=True)
llm_chain = LLMChain(prompt=prompt, llm=llm)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "abc"
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)

class Users(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(250), unique=True, nullable=False)
	password = db.Column(db.String(250), nullable=False)
	chat_messages = db.relationship("ChatMessage", back_populates="user")

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    is_user_message = db.Column(db.Boolean, default=True, nullable=False)

    user = db.relationship("Users", back_populates="chat_messages")


db.init_app(app)


with app.app_context():
	db.create_all()

@login_manager.user_loader
def loader_user(user_id):
	return Users.query.get(user_id)

def parse_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    # Convert the Markdown content to HTML
    html_content = markdown.markdown(content)
    return html_content

def get_article_data():
    # Assuming you have a list of dictionaries containing article titles and image URLs
    # For testing purposes, we'll use hardcoded data here
    article_data = [
        {"title": "Understanding Mental Health", "image_url": "/static/images/article1.jpg"},
        {"title": "Tips for Managing Stress", "image_url": "/static/images/article2.jpg"},
        {"title": "Mental Health Awareness", "image_url": "/static/images/article3.jpg"},
        {"title": "self awarness", "image_url": "/static/images/article3.jpg"},
        {"title": "Health Awareness", "image_url": "/static/images/article2.jpg"}
    ]
    return article_data

@app.route('/')
def home():
    article_data = get_article_data()
    return render_template('home.html', article_data=article_data)

@app.route('/article/<int:article_id>')
def article(article_id):
    article_file = f'data/article{article_id}.md'
    if os.path.exists(article_file):
        article_content = parse_markdown_file(article_file)
        return render_template('article.html', article_content=article_content)
    else:
        return "Article not found."

@app.route('/assistant')
def assistant():
    return render_template('assistant.html')

@app.route('/register', methods=["GET", "POST"])
def register():
	if request.method == "POST":
		user = Users(username=request.form.get("username"),
					password=request.form.get("password"))
		db.session.add(user)
		db.session.commit()
		return redirect(url_for("login"))
	return render_template("sign_up.html")

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		user = Users.query.filter_by(
			username=request.form.get("username")).first()
		if user.password == request.form.get("password"):
			login_user(user)
			return redirect(url_for("home"))
	return render_template("login.html")

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("home"))

@app.route("/Dashboard")
@login_required
def admin_dashboard():
    if current_user.username == 'admin':
        all_users = Users.query.all()
        return render_template("dashboard.html", all_users=all_users)
    else:
        abort(403)

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')
    
@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route("/get")
def get_bot_response():
    userText = str(request.args.get('msg'))
    if userText != "":
        X = vect.transform([userText])
        analysis = ' %s Probability: %.2f%%'%(label[clf.predict(X)[0]],np.max(clf.predict_proba(X))*100)
        ## print the prompt for debug proposes only.
        # print(prompt.format(user=userText, analysis=analysis, system_message=system_message))
        out = llm_chain.run({'user': userText, 'analysis': analysis, 'system_message': system_message})
        message = f'[{analysis}] : {userText}'
        new_message = ChatMessage(user_id=current_user.id, message=message, is_user_message=True)
        db.session.add(new_message)
        chatbot_reply = f'{out}'
        new_reply = ChatMessage(user_id=current_user.id, message=chatbot_reply, is_user_message=False)
        db.session.add(new_reply)
        db.session.commit()

        return str(out)

if __name__ == '__main__':
    app.run(debug=True)