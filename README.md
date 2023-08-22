# Website Categorization

This Python script categorizes a list of websites based on their content using the GPT-3.5 language model from OpenAI. It extracts text content from each website, generates a category using GPT-3, and maps the generated category to predefined categories for better classification.

## Features

- Extracts text content from websites.
- Generates categories using GPT-3.
- Maps categories to predefined categories.
- Saves categorized data in Excel.
- Option to upload data to GitHub.

## How to Use

1. Install required packages:

   ```bash
   pip install openai requests beautifulsoup4 openpyxl pandas
   ```

2. Clone the repo

   ```bash
   git clone https://github.com/maxcodl/Website_Categorizer.git
   ```

6. Replace `openai.api_key` with your API key.

7. Replace `your_ip` with your IP.

8. Add websites to `websites` list.

9. Run the script:

   ```bash
   python app.py
   ```

Script processes websites, generates categories, saves data.


## Flask Web App (Optional)

For a web interface:

1. Install Flask:

   ```bash
   pip install Flask
   ```

2. Create `app.py`.

3. Write Flask app code to display categorized data and provide interface.

4. Run app:

   ```bash
   flask run
   ```

   Access at `http://127.0.0.1:5000/`.

## Credits

Uses GPT-3.5 from OpenAI for website categorization.

Make sure to replace `website_categorization.py` with your actual script name, and create the Flask app code in a separate `app.py` file.
