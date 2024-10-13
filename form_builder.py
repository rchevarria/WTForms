"""
The `FormBuilder` class provides a way to dynamically build and render HTML forms. It allows you to add various types of form questions, such as yes/no, multiple choice, and short text, and then generate the HTML for the form.

The `FormBuilder` class has the following methods:

- `__init__()`: Initializes the `FormBuilder` instance with empty `id_information` and `sections`.
- `add_id(id_label, id_value)`: Adds an ID field to the form with the given label and value.
- `create_section(title)`: Creates a new section in the form with the given title and returns the section object.
- `add_yes_no_question(section, question)`: Adds a yes/no question to the given section.
- `add_multiple_choice_question(section, question, options)`: Adds a multiple choice question to the given section with the specified options.
- `add_short_text_question(section, question)`: Adds a short text question to the given section.
- `to_json()`: Returns a JSON representation of the form data.
- `to_html()`: Generates the HTML for the form based on the form data.

The `generate_form_html()` function takes the JSON representation of the form data and generates the corresponding HTML.
"""
class FormBuilder:
    def __init__(self):
        self.id_information = {}
        self.sections = []

    def add_id(self, id_label, id_value):
        self.id_information[id_label] = id_value

    def create_section(self, title):
        section = {
            "title": title,
            "questions": []
        }
        self.sections.append(section)
        return section

    def add_yes_no_question(self, section, question):
        question_data = {
            "question": question,
            "type": "yes_no"
        }
        section["questions"].append(question_data)

    def add_multiple_choice_question(self, section, question, options):
        question_data = {
            "question": question,
            "type": "multiple_choice",
            "options": options
        }
        section["questions"].append(question_data)

    def add_short_text_question(self, section, question):
        question_data = {
            "question": question,
            "type": "short_text"
        }
        section["questions"].append(question_data)

    def to_json(self):
        return {
            "id_information": self.id_information,
            "sections": self.sections
        }

    def to_html(self):
        form_json = self.to_json()
        return generate_form_html(form_json)

def generate_form_html(form_json):
    html = '<form method="POST">'
    for section in form_json['sections']:
        html += f"<h3>{section['title']}</h3>"
        for question in section['questions']:
            html += f"<label>{question['question']}</label>"
            if question['type'] == 'yes_no':
                html += f"<input type='radio' name='{question['question']}' value='yes'> Yes "
                html += f"<input type='radio' name='{question['question']}' value='no'> No <br>"
            elif question['type'] == 'multiple_choice':
                for option in question['options']:
                    html += f"<input type='checkbox' name='{question['question']}' value='{option}'> {option} "
                html += "<br>"
            elif question['type'] == 'short_text':
                html += f"<input type='text' name='{question['question']}'><br>"
    html += '<button type="submit">Submit Form</button></form>'
    return html
