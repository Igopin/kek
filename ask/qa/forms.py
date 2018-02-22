from django import forms
from qa.models import Question, Answer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.validators import ValidationError



class AskForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    text = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}))

    #def __init__(self, user=None, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    self._user = user

    def save(self):
        self.cleaned_data['author'] = self._user
        print(self.cleaned_data)
        question  = Question(**self.cleaned_data)
        question.save()
        return question

class AnswerForm(forms.Form):
    question = forms.IntegerField()
    text = forms.CharField(label='Comment', widget=forms.Textarea(attrs={"class": "form-control"}))

    def clean(self):
        pass

    def get_question_url(self):
        return self.cleaned_data['question'].get_url()

    def save(self):
        self.cleaned_data['question'] = Question.objects.get(pk=self.cleaned_data['question']) 
        self.cleaned_data['author'] = self._user
        print(self.cleaned_data)
        answer = Answer(**self.cleaned_data)
        answer.save()
        return answer


class SignUpForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    def save(self):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password'],
            )
        user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

    def clean(self):
        user = authenticate(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        if user is not None:
            self.cleaned_data['user'] = user
        else:
            raise ValidationError('Login or password is incorrect!')


    def get_user(self):
        return self.cleaned_data['user']