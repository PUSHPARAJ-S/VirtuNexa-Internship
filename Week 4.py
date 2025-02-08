import requests
from bs4 import BeautifulSoup
import sqlite3
from flask import Flask, render_template, request

# Initialize Flask app
app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY,
            title TEXT,
            link TEXT,
            category TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS preferences (
            id INTEGER PRIMARY KEY,
            keyword TEXT
        )
    """)
    conn.commit()
    conn.close()

# Function to scrape news
def scrape_news():
    url = "https://www.bbc.com/news"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = soup.find_all("h3")
    
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()
    
    for h in headlines[:10]:  # Get top 10 headlines
        title = h.text.strip()
        link = "https://www.bbc.com" + h.find_parent("a")["href"]
        cursor.execute("INSERT INTO news (title, link, category) VALUES (?, ?, ?)", (title, link, "General"))
    
    conn.commit()
    conn.close()

# Function to get personalized news
def get_personalized_news():
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()
    cursor.execute("SELECT keyword FROM preferences")
    keywords = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT title, link FROM news")
    news = cursor.fetchall()
    
    filtered_news = [n for n in news if any(k.lower() in n[0].lower() for k in keywords)]
    conn.close()
    return filtered_news if filtered_news else news  # Return all news if no match

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        keyword = request.form.get("keyword")
        if keyword:
            conn = sqlite3.connect("news.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO preferences (keyword) VALUES (?)", (keyword,))
            conn.commit()
            conn.close()
    news = get_personalized_news()
    return render_template("index.html", news=news)

if __name__ == "__main__":
    init_db()
    scrape_news()
    app.run(debug=True)

# Procedure to  see the scraped news
# Open the broswer and visit the url http://127.0.0.1:5000/