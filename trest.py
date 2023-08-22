import openai
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
import pandas as pd

# Set your OpenAI API key
openai.api_key = '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'
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
"react-icons.github.io",
"docusign.com",
"macreports.com",
"insider.com",
"playgabu.com",
"hammondsflycatcher.com",
"therundown.ai",
"atlantatechvillage.com",
"business-software.com",
"qualtrics.com",
"sstech.us",
"piedmontpark.org",
"beebom.com",
"artificiallawyer.com",
"atldistrict.com",
"trustradius.com",
"invisors.com",
"bart.gov",
"insightglobal.com",
"kseb.in",
"rbccm.com",
"fast.com",
"sandheep.com",
"theverge.com",
"healthline.com",
"cointelegraph.com",
"trinamix.com",
"enquero.com",
"aiscovery.com",
"gegainfotech.com",
"technology-holdings.com",
"deccanchronicle.com",
"soltech.net",
"njtransit.com",
"prutech.com",
"intuit.com",
"builtin.com",
"katiecaftravel.com",
"uxdesign.cc",
"bookandlink.com",
"crunchbase.com",
"atvubud.com",
"themanifest.com",
"innowise-group.com",
"worldtimebuddy.com",
"tablericons.com",
"tabler-icons.io",
"tips-and-tricks.co",
"claude.ai",
"qodeca.com",
"simpleflying.com",
"kannan.co",
"miami-airport.com",
"dreamfolks.in",
"pedicon2024.com",
"chittilappillysquare.com",
"hexnode.com",
"netlinkdigitalsolutions.com",
"enhops.com",
"navantpartners.com",
"incomm.com",
"bluewatersinvestment.com",
"5-capital.com",
"7mileadvisors.com",
"hl.com",
"leonispartners.com",
"corumgroup.com",
"sequelize.org",
"channele2e.com",
"meta.com",
"infosys.com",
"tracxn.com",
"kpmg.us",
"aventis-advisors.com",
"speedtest.net",
"tenorshare.com",
"mindvalley.com",
"instructables.com",
"ondc.org",
"startupindia.gov.in",
"bhaskar.com",
"rapidtables.com",
"ipocentral.in",
"phantombuster.com",
"ezeshas.com",
"vic.ai",
"ellow.io",
"inflection.io",
"ghcgrowthlab.com",
"maxio.com",
"kruzeconsulting.com",
"mygreatlearning.com",
"workday.com",
"certinia.com",
"meetalfred.com",
"pornhub.com",
"klazify.com",
"tiluf.com",
"stackblitz.com",
"semrush.com",
"ahrefs.com",
"xhamster.com",
"profitwell.com",
"miro.com",
"huggingface.co",
"deepai.org",
"convertcsv.com",
"deepdreamgenerator.com",
"topten.ai",
"regex101.com",
"arxiv.org",
"paperswithcode.com",
"xvideos.com"
"roboquery.com",
"yoast.com",
"cbic.gov.in",
"groww.in",
"siteslike.com",
"thequint.com",
"intelliswift.com",
"insent.ai",
"zpodz.in",
"finead.gr",
"ascendion.com",
"orionsoftware.com",
"orioninc.com",
"census2011.co.in",
"mphasis.com",
"mergr.com",
"prnewswire.com",
"vrize.com",
"envu.com",
"cognicor.com",
"sciencealert.com",
"harvey.ai",
"sequoiacap.com",
"legalitprofessionals.com",
"lawnext.com",
"arctitan.com",
"criticalriver.com",
"fresherslive.com",
"persianbasketatl.com"
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
        prompt = f"this is a website [{url}]. and this is the content i extracted from the website: [{text_content}]. Can you tell which category this website belongs to by reading the content from the website? i want the result in a json format ('website': 'website_name', 'category': 'category_name') like the following.while picking the category, only use the ones provided below (Technology,Startup,Sales,Health,Business,Education,Finance,Web3,Human Resource,Generative AI,Others,Economy,Gen AI,HR,Law,Management,Productivity,Sales & Marketing,Stocks, Tech,VC & PE, Adult)"
        
        # Use OpenAI to generate the category
        response = openai.ChatCompletion.create(
            model=model_engine,
            temperature=0.5,
            top_p=0,
            max_tokens=50,
            presence_penalty=0,
            frequency_penalty=0,
            messages=[{"role": "system", "content": "You are an expert website classifier."},
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