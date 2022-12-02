from django import forms

class FileForm(forms.Form):
    file_upload = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )