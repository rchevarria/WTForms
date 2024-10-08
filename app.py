import os
import json
from flask import Flask, render_template, request
from wtforms import Form, StringField, RadioField
from wtforms.validators import DataRequired

app = Flask(__name__)

def create_dynamic_form(json_data):
    # Create a dictionary to hold dynamically created form fields
    form_fields = {}

    for idx, item in enumerate(json_data["items"]):
        title = item.get("title", f"Question {idx + 1}")  # Default title if missing
        question_item = item.get("questionItem")  # Safely get questionItem
        
        if question_item is None:
            continue  # Skip this item if questionItem is missing
        
        question = question_item.get("question")

        # Check the type of question and create fields accordingly
        if "textQuestion" in question:
            field = StringField(title, [DataRequired()] if question["required"] else [])
        elif "choiceQuestion" in question_item:
            options = [
                (option["value"], option["value"]) 
                for option in question_item["choiceQuestion"]["options"]
            ]
            field = RadioField(title, choices=options, default=options[0][0], 
                               validators=[DataRequired()] if question["required"] else [])

        # Use a unique key for each field to avoid duplicates
        form_fields[f"{title}_{idx}"] = field  # Adding index to title

    # Create a new form class with the dynamically created fields
    DynamicForm = type('DynamicForm', (Form,), form_fields)
    return DynamicForm



@app.route('/', methods=['GET', 'POST'])
def index():
    # Load the JSON data from the community_engagement_survey.json file
    json_file_path = os.path.join('example_forms', 'community_engagement_survey.json')
    
    with open(json_file_path) as json_file:
        json_data = json.load(json_file)
        print(json_data)
    
    # Create the dynamic form class
    DynamicFormClass = create_dynamic_form(json_data)
    
    # Instantiate the form class
    form = DynamicFormClass(request.form)

    if request.method == 'POST' and form.validate():
        # Process form data here
        return "Form submitted successfully!"  # You can process the data as needed

    return render_template('form.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
