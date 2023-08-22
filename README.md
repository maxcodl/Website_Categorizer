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

2. Replace `openai.api_key` with your API key.

3. Add websites to `websites` list.

4. Run the script:

   ```bash
   python website_categorization.py
   ```

   Script processes websites, generates categories, saves data.

5. To upload data to GitHub:

   - Replace repository URL in script.
   - Run script to save data to repository.

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

## License

This project is licensed under the [MIT License](LICENSE).
```

Make sure to replace `website_categorization.py` with your actual script name, and create the Flask app code in a separate `app.py` file.
