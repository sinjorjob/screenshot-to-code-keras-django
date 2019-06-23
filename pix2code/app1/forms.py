
from django import forms
from .models import Document
from upload_validator import FileTypeValidator

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('document', )
    
    
    document = forms.FileField(label="File Upload",
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        validators=[FileTypeValidator(allowed_types=[ 'image/png'])])

        
