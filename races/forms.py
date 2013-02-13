"""
forms.py

Created by Devin Breen on 2012-02-22.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

from django import forms

class SelectedRouteForm(forms.Form):
    selected = forms.BooleanField(required=False)
    
