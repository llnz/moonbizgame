
from django import forms

from enterprise.models import Enterprise

class EnterpriseAddForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    
    start_cash = forms.ChoiceField(choices=[(500000000, 'Easy'),
                                            (100000000, 'Medium'),
                                            (50000000, 'Hard')], label="Difficulty")
    
    class Meta:
        model = Enterprise
        exclude = ('owners', 'universe', 'slug', 'mode', 'created_irl', 'created_igt')
