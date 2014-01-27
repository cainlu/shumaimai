from django import forms

class SellForm(forms.Form):
    sellformphone = forms.IntegerField(min_value=0)
    sellformaddress = forms.CharField()
    sellformremark = forms.CharField(required=False)
