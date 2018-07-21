from django import forms

from when_the_light_go_down.models import Fiche


class FicheForm(forms.ModelForm):
    class Meta:
        model = Fiche
        fields = '__all__'
        widgets = {
            'nom_perso': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'prenom_perso': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'description_perso': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
            }),
        }
