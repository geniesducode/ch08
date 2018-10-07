from django import forms


class NameForm(forms.Form):
    # La longueur maximale du champ doit correspondre à celle définie dans models.py sur l'attribut Result.name
    name = forms.CharField(label="Votre nom", max_length=50)
