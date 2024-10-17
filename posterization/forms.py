from django import forms

class PosterForm(forms.Form):
  pdf_file = forms.FileField()
  
  # Add the following fields to the PosterForm rows and cols class with choices of 1 - 6
  rows = forms.ChoiceField(choices=[(i, i) for i in range(1, 7)], initial=1, label='Linhas')
  cols = forms.ChoiceField(choices=[(i, i) for i in range(1, 7)], initial=1, label='Colunas')