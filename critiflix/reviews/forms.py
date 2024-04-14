from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(required=False, min_length=3)
    search_in = forms.ChoiceField(required=False,
                                  choices=(
                                      ("movie_name", "Tytuł"),
                                      ("actor", "Aktor")
                                  ))
