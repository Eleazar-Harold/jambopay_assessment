from typing import Any
from django import forms
from django.core.validators import FileExtensionValidator

# CSV Import form
class CSVImportForm(forms.Form):
    csv_file =  forms.FileField(label="Upload CSV File", validators=[FileExtensionValidator(['csv'])])
