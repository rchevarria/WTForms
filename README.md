# Alternative to Google forms

# Flask WTForms Example with Supabase Integration

This is a simple Flask application that demonstrates how to create a form using Flask-WTF and integrate it with a Supabase database.

## Prerequisites

- Python 3.x
- Pip (Python package installer)
- Supabase account and project

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/flask-wtforms-supabase.git
    cd flask-wtforms-supabase
    ```

2. **Create and activate a virtual environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:

    Create a `.env` file in the project root directory and add your Supabase URL and API key:

    ```text
    SUPABASE_URL='your_supabase_url'
    SUPABASE_KEY='your_supabase_key'
    ```
4a. Set up secret key
cd root directory
 ```
python
import os
print(os.urandom(24).hex())
 ```

5. **Update the Flask secret key**:

    Open `app.py` and update the `SECRET_KEY` value:

    ```python
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    ```

## Running the Application

1. **Run the Flask application**:

    ```bash
    python app.py
    ```

2. **Open your browser** and navigate to `http://127.0.0.1:5000/` to see the form.

## Project Structure

- `app.py`: The main Flask application file.
- `templates/`: Directory containing the HTML templates.
  - `index.html`: The form template.
  - `success.html`: The success page template.
- `.env`: File containing environment variables (not included in version control).
- `requirements.txt`: List of Python dependencies.

## Dependencies

- Flask
- Flask-WTF
- requests
- python-dotenv

## Example .env File

```text
SUPABASE_URL='https://xyzcompany.supabase.co'
SUPABASE_KEY='your-super-secret-api-key'
