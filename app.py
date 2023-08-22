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
        text_content = " ".join(text_content.split())

        # List of categories and related keywords
        categories_keywords = {
            "Jobs & Education": ["Education", "Colleges & Universities", "Distance Learning","Homeschooling", "Primary & Secondary Schooling (K-12)","Standardized & Admissions Tests", "Teaching & Classroom Resources","Training & Certification","Vocational & Continuing Education","Jobs", "Career Resources & Planning","Job Listings","Resumes & Portfolios"],
            "Law & Government": ["Government","Courts & Judiciary","Visa & Immigration","Legal","Bankruptcy","Legal Education","Legal Services","Military","Public Safety","Crime & Justice", "Emergency Services",  "Law Enforcement", "Security Products & Services",  "Social Services"],
            "Arts & Entertainment": [ "Anime & Manga","Acting & Theater","Architecture","Art Museums & Galleries","Bars, Clubs & Nightlife","Cartoons","CD & Audio Shopping","Circus","Classical Music","Comics","Concerts & Music Festivals","Country Music","Dance","Dance & Electronic Music","Design","Experimental & Industrial Music","Expos & Conventions","Film & TV Industry","Film Festivals","Flash-Based Entertainment","Fun Tests & Silly Surveys","Funny Pictures & Videos","Jazz & Blues","Magic","Movie Listings & Theater Showtimes","Music Education & Instruction","Music Equipment & Technology","Music Reference","Music Streams & Downloads","Music Videos","Occult & Paranormal","Online Image Galleries","Online Video","Opera","Painting","Photographic & Digital Arts","Political Humor","Pop Music","Radio","Recording Industry","Religious Music","Rock Music","Soundtracks","TV Commercials","TV Shows & Programs","Urban & Hip-Hop","World Music"],
            "Adult": ["Adult", "Porn","Creampie","Lesbian"],
            "Autos & Vehicles": ["Bicycles & Accessories","Bike Parts & Repair","BMX Bikes","Boats & Watercraft","Campers & RVs","Cargo Trucks & Trailers","Classic Vehicles","Commercial Vehicles","Gas Prices & Vehicle Fueling","Hybrid & Alternative Vehicles","Motor Vehicles (By Type)","Motorcycles","Off-Road Vehicles","Trucks & SUVs","Used Vehicles","Vehicle Codes & Driving Laws","Vehicle Licensing & Registration","Vehicle Parts & Accessories","Vehicle Parts & Services","Vehicle Repair & Maintenance","Vehicle Shopping","Vehicle Shows"],
            "Beauty & Fitness": ["Beauty Pageants","Body Art","Cosmetic Procedures","Cosmetology & Beauty Professionals","Face & Body Care","Fashion & Style","Fitness","Hair Care","Spas & Beauty Services","Weight Loss","Cosmetic Surgery","Hygiene & Toiletries","Make-Up & Cosmetics","Perfumes & Fragrances","Skin & Nail Care","Unwanted Body & Facial Hair Removal","Fashion Designers & Collections","Hair Loss","Massage Therapy"],
            "Business & Industrial": ["Advertising & Marketing","Aerospace & Defense","Agriculture & Forestry","Automotive Industry","Business Education","Business Finance","Business Operations","Business Services","Chemicals Industry","Construction & Maintenance","Energy & Utilities","Hospitality Industry","Industrial Materials & Equipment","Manufacturing","Metals & Mining","Pharmaceuticals & Biotech","Printing & Publishing","Retail Trade","Small Business","Textiles & Nonwovens","Transportation & Logistics","Public Relations","Space Technology","Agricultural Equipment","Forestry","Livestock","Venture Capital","Business Plans & Presentations","Management","Consulting","Corporate Events","E-Commerce Services","Fire & Security Services","Office Services","Office Supplies","Writing & Editing Services","Cleaning Agents","Plastics & Polymers","Building Materials & Supplies","Electricity","Oil & Gas","Renewable & Alternative Energy","Event Planning","Food Service","Heavy Machinery","Precious Metals","Retail Equipment & Technology","MLM & Business Opportunities","Freight & Trucking","Mail & Package Delivery","Maritime Transport","Moving & Relocation","Packaging","Parking","Rail Transport","Urban Transport"]
        }

        # Function to check the extracted text for specific keywords and assign a category
        def categorize_based_on_keywords(text, categories_keywords):
            matched_categories = []
            for category, keywords in categories_keywords.items():
                matched_keywords = [keyword for keyword in keywords if keyword.lower() in text.lower()]
                if len(matched_keywords) >= 3:
                    matched_categories.append(category)
                if not matched_categories:
                    print("No keywords found in the text.")
            return matched_categories

        # Check if we can categorize based on keywords
    categories = categorize_based_on_keywords(text_content, categories_keywords)

    if categories:
        print(f"Categories assigned based on keyword match: {categories}")
        return render_template('result.html', website=url, category=categories, source="keyword")

    elif not categories and text_content:
        print("No category was assigned based on keywords. Using OpenAI to categorize.")
    # After receiving response from OpenAI
        

    # If no category found using keywords and text_content exists, then use OpenAI
    if not categories and text_content:
        if text_content is not None:
            text_content = " ".join(text_content.split())
            # Limit the text content to 500 words
        word_limit = 600
        if len(text_content.split()) > word_limit:
            text_content = " ".join(text_content.split()[:word_limit])
        # Create a prompt for OpenAI categorization
        prompt = (
        f"This is a website [{url}], and this is the content I extracted from the website: [{text_content}]. "
        "Can you determine which category this website belongs to based on the content? "
        "I would like the result in JSON format as follows: "
        "'website': 'url', 'category': 'category_name'. "
        "Please choose a category from the list provided below for accurate classification: "
        "(Technology, Startup, Sales, Health, Business, Education, Finance, Web3, Human Resource, Generative AI, Others, Economy, Gen AI, HR, Law, Management, Productivity, Sales & Marketing, Stocks, Tech, VC & PE, Entertainment, Adult). "
        "You can select multiple categories if you are familiar with the website. "
        "You may also disregard the extracted data if necessary. "
        "IMPORTANT: While showing the result, only show the json result."
    )
        # Log the prompt being sent to OpenAI
        print("Prompt to OpenAI:", prompt)

        # Use OpenAI to generate the category
        response = openai.ChatCompletion.create(
        model=model_engine,
        temperature=0.8,
        top_p=1,
        max_tokens=50,
        presence_penalty=0,
        frequency_penalty=0.57,
        messages=[{"role": "system", "content": "You are an expert in website categorization."},
                  {"role": "assistant", "content": "{'website': 'url', 'category': 'category_name'}"},
                  {"role": "user", "content": prompt}]
    )

        chosen_categories = response['choices'][0]['message']['content'].split(',')

        # Log the response received from OpenAI
        print("Response from OpenAI:", response)

        return render_template('result.html', website=url, category=chosen_categories, source="openai")
    else:
        return "Failed to extract text from the website"


# Run the Flask app
if __name__ == '__main__':
    app.run()
