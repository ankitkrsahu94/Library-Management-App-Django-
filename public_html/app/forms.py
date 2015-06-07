from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from app.models import *

class UserForm(ModelForm):
	password = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))
	password1 = forms.CharField(label=(u'Verify Password'), widget=forms.PasswordInput(render_value=False))
	
	class Meta:
		model = User
		fields = ('username','email','password','password1','first_name','last_name')

class UserProfileForm(ModelForm):
	class Meta:
		model = Member
		fields = ('dob',)


class BookForm(ModelForm):
	class Meta:
		model = Book
		fields = ('isbn','title','pub_date','author','category','quantity','available')