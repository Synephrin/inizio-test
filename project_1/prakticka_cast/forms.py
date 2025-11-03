from django import forms

class SearchedPhrase(forms.Form):
    input_text= forms.CharField(label="Hledaná fráze", required=True, max_length=50)