import openai
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
import pandas as pd

# Set your OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'
model_engine = "gpt-3.5-turbo-16k"

category_mapping = {
    "technology": "Technology",
    "startup": "Startup",
    "sales": "Sales",
    "health": "Health",
    "business": "Business",
    "education": "Education",
    "finance": "Finance",
    "web3": "Web3",
    "human resource": "Human Resource",
    "generative ai": "Generative AI",
    "economy": "Economy",
    "gen ai": "Gen AI",
    "hr": "HR",
    "law": "Law",
    "management": "Management",
    "productivity": "Productivity",
    "sales & marketing": "Sales & Marketing",
    "stocks": "Stocks",
    "tech": "Tech",
    "vc & pe": "VC & PE",
}
# Create an empty list to store data
data = []


# List of websites to extract data from
websites = [ 
    'list of websites'
]


# Create a pandas DataFrame to store data
columns = ["URL", "Request", "Response", "Extracted Data"]
df = pd.DataFrame(columns=columns)


# Function to extract text from a website
def extract_text_from_website(url):
    try:
        response = requests.get(url, timeout=10)  # Set a timeout value in seconds
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            all_text = ' '.join([element.get_text() for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'span'])])
            return all_text
        else:
            return None
    except requests.exceptions.Timeout:
        print(f"Timeout error: Could not connect to {url}")
        return None
    except Exception as e:
        print("Error:", e)
        return None



# Iterate through the list of websites
for website in websites:
    url = f"https://{website}"
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
        
        generated_category = response['choices'][0]['message']['content']

        # Map the generated category to predefined categories
        if generated_category in category_mapping:
            category = category_mapping[generated_category]
        else:
            category = "Others"
        # Append data to the list
        data.append({"URL": url, "Request": prompt, "Generated Category": generated_category, "Category": category, "Extracted Data": text_content})
        
        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(data)
        
        # Save the data to an Excel file after each request
        df.to_excel("website_data_temp.xlsx", index=False)
        
        print(f"Processed {url}")
        
        # Add a delay to avoid overloading the server
        time.sleep(5)
    else:
        print(f"Failed to extract text from {url}")

# Save the final data to an Excel file
df.to_excel("website_data.xlsx", index=False)
print("Final data saved to website_data.xlsx")
