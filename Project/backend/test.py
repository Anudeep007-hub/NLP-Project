from bs4 import BeautifulSoup as bs
import requests
from flask import Flask, jsonify 
from flask_cors import CORS
import os




app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}) # Allowing the cross origin requests 



def parse_url_MICROSOFT(url):
    response = requests.get(url) 
    soup = bs(response.content, "lxml") 
    article = soup.find(name="article", class_ = "ocpArticleContent")

    for script in article(["script", "style"]):
            script.extract()


        # Get textual content
    text = article.get_text(separator=' ')
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)

    if not text:
        return f" <h3> Article not found with the url:{url} <h3>"
    return text


def parse_url_LINUS(url):   # Send a request to get the forum page
    response = requests.get(url)
    soup = bs(response.content, "lxml")

    # Find all threads in the laptop forum
    threads = soup.find_all("div", class_="structItem-title")
    
    if not threads:
        return f"<h3> No threads found on the page: {url} </h3>"

    # Start building the HTML string with the parsed threads
    html_output = "<ul>\n"
    for thread in threads:
        # Extract the thread title and URL
        title = thread.get_text(strip=True)
        url = "https://forums.tomshardware.com" + thread.find("a")["href"]
        # Append each thread as a list item in the HTML string
        html_output += f"<li><a href='{url}'>{title}</a></li>\n"
    html_output += "</ul>"

    return html_output



@app.route("/api/answer", methods = ["GET"]) 
def get_answer():
    # url = "https://support.microsoft.com/en-us/windows/resolving-blue-screen-errors-in-windows-60b01860-58f2-be66-7516-5c45a66ae3c6"
    url = "https://support.microsoft.com/en-us/help/4028544/windows-10-allow-blocked-firewall-apps  "
    # answer_page = parse_url_MICROSOFT(url) \
    answer_page = None
    if "microsoft" in url:
        answer_page = parse_url_MICROSOFT(url) 
    elif "linustechtips" in url:
        answer_page = parse_url_LINUS(url)
    print(answer_page)
    return answer_page 

if __name__ == "__main__":
    app.run(debug=True)


    

