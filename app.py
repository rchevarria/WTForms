from flask import Flask, render_template, request
from wtforms import Form, StringField, RadioField, BooleanField, validators

app = Flask(__name__)

def create_dynamic_form(json_data):
    # Dynamically create form fields
    fields = {}
    for idx, item in enumerate(json_data['items']):
        field_title = item.get('title', 'Field')  # Default title if not found
        required = False  # Default to not required

        # Check if 'questionItem' and 'question' exist
        question_item = item.get('questionItem', {})
        question = question_item.get('question', {})

        if 'required' in question:
            required = question['required']

        if 'textQuestion' in question:
            fields[f'field_{idx}'] = StringField(
                field_title, 
                validators=[validators.InputRequired()] if required else []
            )
        elif 'choiceQuestion' in question:
            options = [(option['value'], option['value']) for option in question['choiceQuestion']['options']]
            if question['choiceQuestion']['type'] == 'RADIO':
                fields[f'field_{idx}'] = RadioField(
                    field_title, 
                    choices=options, 
                    default=None
                )
            elif question['choiceQuestion']['type'] == 'CHECKBOX':
                fields[f'field_{idx}'] = BooleanField(field_title)

    # Create the form class with the dynamically created fields
    DynamicFormClass = type('DynamicForm', (Form,), fields)
    return DynamicFormClass


@app.route('/', methods=['GET', 'POST'])
def index():
    # Sample JSON data
    json_data = {
        "items": [
            {
                "title": "What is your full name?",
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "What is your email address?",
                "questionItem": {
                    "question": {
                        "required": True,
                        "textQuestion": {
                            "paragraph": False
                        }
                    }
                }
            },
            {
                "title": "Which service did you find most beneficial?",
                "questionItem": {
                    "required": True,
                    "choiceQuestion": {
                        "type": "RADIO",
                        "options": [
                            { "value": "Healthcare" },
                            { "value": "Education" },
                            { "value": "Public Safety" },
                            { "value": "Environmental Protection" }
                        ],
                        "shuffle": True
                    }
                }
            },
            # Add more items as needed...
        ]
    }
    
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
