from flask import Flask, render_template, request, redirect
from wtforms import StringField, RadioField, BooleanField, SelectField, validators
from flask_wtf import FlaskForm
import json
import os
from wtforms import SelectMultipleField, widgets

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['WTF_CSRF_ENABLED'] = False

# Ensure the upload directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def create_dynamic_form(json_data):
    """Dynamically create a WTForm class from the JSON structure."""
    
    # Create a dictionary to hold the fields
    form_fields = {}

    # Extract title and description from the 'info' section
    form_info = json_data.get('info', {})
    form_title = form_info.get('title', 'Default Title')
    form_description = form_info.get('description', 'Default Description')

    # Create fields for title and description
    form_fields['title'] = form_title  # Keep this as a string, not a field
    form_fields['description'] = form_description  # Keep this as a string, not a field

    for idx, item in enumerate(json_data['items']):
        # Check for 'questionItem' to skip non-question items like page breaks
        question_item = item.get('questionItem')
        if not question_item:
            continue  # Skip this item if 'questionItem' is missing

        question = question_item.get('question', {})
        field_title = item.get('title', f'Field {idx}')
        required = question.get('required', False)

        if 'textQuestion' in question:
            # Handling text questions (with and without paragraphs)
            form_fields[f'field_{idx}'] = StringField(
                field_title, 
                validators=[validators.InputRequired()] if required else []
            )
        elif 'choiceQuestion' in question:
            # Handling choice questions (radio, checkbox, dropdown)
            options = [(option['value'], option['value']) for option in question['choiceQuestion']['options']]
            choice_type = question['choiceQuestion'].get('type')
            
            if choice_type == 'RADIO':
                form_fields[f'field_{idx}'] = RadioField(
                    field_title, 
                    choices=options, 
                    validators=[validators.InputRequired()] if required else []
                )
            elif choice_type == 'CHECKBOX':
                # Handle multiple checkboxes using SelectMultipleField
                form_fields[f'field_{idx}'] = SelectMultipleField(
                    field_title,
                    choices=options,
                    option_widget=widgets.CheckboxInput(),
                    widget=widgets.ListWidget(prefix_label=False),
                    validators=[validators.InputRequired()] if required else []
                )
            elif choice_type == 'DROP_DOWN':
                form_fields[f'field_{idx}'] = SelectField(
                    field_title, 
                    choices=options, 
                    validators=[validators.InputRequired()] if required else []
                )
    
    # Dynamically create a Form class inheriting from FlaskForm
    DynamicForm = type('DynamicForm', (FlaskForm,), form_fields)
    return DynamicForm, form_title, form_description


@app.route('/', methods=['GET', 'POST'])
def index():
    form = None
    form_title = ''
    form_description = ''
    
    if request.method == 'POST' and 'json_file' in request.files:
        file = request.files['json_file']
        if file and file.filename.endswith('.json'):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Read and parse the JSON file
            with open(file_path, 'r') as f:
                json_data = json.load(f)

            # Generate the form dynamically based on the JSON
            DynamicFormClass, form_title, form_description = create_dynamic_form(json_data)
            form = DynamicFormClass(request.form)

            if form.validate_on_submit():
                # Process form submission here
                print("Form submitted successfully!")
                print("Submitted Data:", {field.name: field.data for field in form})
                return "Form submitted successfully!"

    return render_template('form.html', form=form, form_title=form_title, form_description=form_description)

if __name__ == '__main__':
    app.run(debug=True)
