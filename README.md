
# Website Categorization

This Python script and Flask web application categorize websites based on their content using the GPT-3.5 language model from OpenAI. It extracts text content from each website, generates a category using GPT-3, and maps the generated category to predefined categories for accurate classification.

## Features

- Extracts text content from websites.
- Generates categories using GPT-3.
- Maps categories to predefined categories.
- Provides both a command-line script and a Flask web interface.
- Saves categorized data.

## How to Use the Command-Line Script

1. Install required packages:

   ```bash
   pip install openai requests beautifulsoup4 openpyxl pandas
   ```

2. Clone the repository:

   ```bash
   git clone https://github.com/maxcodl/Website_Categorizer.git
   ```

3. Replace `'YOUR_OPENAI_API_KEY'` in the `app.py` script with your actual OpenAI API key.

4. Add websites to the `websites` list in the `app.py` script.

5. Run the script:

   ```bash
   python app.py
   ```

   The script will process websites, generate categories, and save categorized data.

## Flask Web App (Optional)

For a more user-friendly interface, you can set up a Flask web application:

1. Install Flask:

   ```bash
   pip install Flask
   ```

2. Create `app.py`.

3. Write Flask app code to display categorized data and provide an interface for users.

4. Run the Flask app:

   ```bash
   flask run
   ```

   Access the app at `http://127.0.0.1:5000/`.

## Credits

This project utilizes the GPT-3.5 model from OpenAI for website categorization.

Make sure to replace `'app.py'` with your actual script name and create the Flask app code in a separate `'app.py'` file.
```

Make sure to replace `'YOUR_OPENAI_API_KEY'` with your actual OpenAI API key in the script.
