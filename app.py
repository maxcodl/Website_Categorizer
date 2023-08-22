from flask import Flask, render_template, request
import openai
import requests
from bs4 import BeautifulSoup
import time 
from urllib.parse import urlparse
app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'
model_engine = "gpt-3.5-turbo-16k"


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/categorize', methods=['POST'])
def categorize():
    url = request.form['url']

    # Check if the input URL starts with "http" or "www"
    if not url.startswith(('http', 'www')):
        # Assuming it's a hostname without the "https://" prefix
        url = f"https://{url}"

    # Add a delay to allow the website to load
    time.sleep(5) 

    # Function to extract text from a website
    def extract_text_from_website(url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                all_text = ' '.join([element.get_text() for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'span'])])
                return all_text
            else:
                return None
        except Exception as e:
            print("Error:", e)
            return None

    # Extract text content from the website
    text_content = extract_text_from_website(url)

    if text_content is not None:
        # Create a prompt for OpenAI categorization
        prompt = (
        f"This is a website [{url}], and this is the content I extracted from the website: [{text_content}]. "
        "Can you determine which category this website belongs to based on the content? "
        "I would like the result in JSON format as follows: "
        "'website': 'url', 'category': 'category_name'. "
        "Please choose a category from the list provided below for accurate classification: "
        "(Technology, Startup, Sales, Health, Business, Education, Finance, Web3, Human Resource, Generative AI, Others, Economy, Gen AI, HR, Law, Management, Productivity, Sales & Marketing, Stocks, Tech, VC & PE, Adult). "
        "You can select multiple categories if you are familiar with the website. "
        "You may also disregard the extracted data if necessary. "
        "IMPORTANT: While showing the result, only show the json."
    )
        # Log the prompt being sent to OpenAI
        print("Prompt to OpenAI:", prompt)

        # Use OpenAI to generate the category
        response = openai.ChatCompletion.create(
        model=model_engine,
        temperature=0.8,
        top_p=1,
        max_tokens=30,
        presence_penalty=0,
        frequency_penalty=0.57,
        messages=[{"role": "system", "content": "You are an expert in website categorization."},
                  {"role": "assistant", "content": "{'website': 'url', 'category': 'Finance'}"},
                  {"role": "user", "content": prompt}]
    )

        category = response['choices'][0]['message']['content']

        # Log the response received from OpenAI
        print("Response from OpenAI:", response)

        return render_template('result.html', category=category)
    else:
        return "Failed to extract text from the website"


# Run the Flask app
if __name__ == '__main__':
    app.run()
