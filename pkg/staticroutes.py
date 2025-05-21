from flask import render_template,request,flash,url_for,redirect,session
from werkzeug.security import generate_password_hash,check_password_hash
from pkg import app,forms
from pkg.models import db,User
from datetime import datetime
import openai
from dotenv import load_dotenv
import os
load_dotenv()

@app.route("/")
def home():
   return render_template("index.html",)




@app.route("/login/", methods=["GET", "POST"])
def login():
    form=forms.LoginForm()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.user_id
            flash("Logged in successfully!", "success")
            return redirect(url_for("chat"))
        else:
            flash("Invalid email or password.", "danger")
            return redirect(url_for("login"))
    return render_template("login.html",form=form)



@app.route("/register/", methods=["GET", "POST"])
def register():
    regform=forms.RegistrationForm()
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered.", "danger")
            return redirect(url_for("register"))
        # Create new user
        new_user = User(
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html",regform=regform)



@app.route("/logout/")
def logout():
    session.pop("user_id", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))







@app.route("/chat/", methods=["GET", "POST"])
def chat():
    chat = forms.ChatForm()
    if "user_id" not in session:
        flash("Please log in to access the chat.", "warning")
        return redirect(url_for("login"))
    user_id = session["user_id"]
    deets = db.session.query(User).get(user_id)

    messages = []
    if request.method == "POST":
        user_prompt = request.form.get("prompt")
        messages.append({"role": "user", "content": user_prompt})

        # Call OpenAI API with error handling for quota/rate limits
        client = openai.OpenAI(api_key="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")
        # Ensure you have set your OpenAI API key in the environment variables
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_prompt}
                ]
            )
            ai_reply = response.choices[0].message.content
        except openai.RateLimitError:
            ai_reply = "Sorry, the AI service is currently unavailable due to quota limits. Please try again later."
        except Exception as e:
            ai_reply = f"An error occurred: {str(e)}"
        messages.append({"role": "ai", "content": ai_reply})

    return render_template("chatpage.html", deets=deets, messages=messages, chat=chat)

