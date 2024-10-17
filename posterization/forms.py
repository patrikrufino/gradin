from django import forms

class PosterForm(forms.Form):
  pdf_file = forms.FileField(
    label='Arquivo PDF', 
    required=True,
    widget=forms.ClearableFileInput(attrs={
      'accept': 'application/pdf', 
      'class': ('btn-blue form-control-file text-sm capitalize border-2 p-1 rounded-md justify-between min-w-full'),
      }),
    error_messages={'required': 'Por favor, selecione um arquivo PDF.'},
    help_text='Selecione um arquivo PDF para ser convertido em um poster.'
    )
  
  # Add the following fields to the PosterForm rows and cols class with choices of 1 - 6
  rows = forms.ChoiceField(choices=[(i, i) for i in range(1, 7)], initial=1, label='Linhas')
  cols = forms.ChoiceField(choices=[(i, i) for i in range(1, 7)], initial=1, label='Colunas')