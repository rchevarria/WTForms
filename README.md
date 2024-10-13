# Alternative to Google forms

# Flask WTForms Example 

This is a simple Flask application that demonstrates how to create a form using Flask-WTF.

## Prerequisites

- Python 3.x
- Pip (Python package installer)

## Installation

1. **Clone the repository**:

    ```bash
    git clone 
    cd 
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

