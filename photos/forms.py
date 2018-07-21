from django import forms


class RegisterForm(forms.Form):
    name = forms.CharField(max_length=45, label="",
                           widget=forms.TextInput(attrs={"placeholder": "Username", "class": "form-control"}))
    password = forms.CharField(max_length=45, label= "",
                            widget=forms.TextInput(attrs={"placeholder":"Password", "type":"password", "class": "form-control"}))
    email = forms.CharField(max_length=255, label="",
                          widget=forms.TextInput(attrs={"placeholder": "email", "class": "form-control"}))


class LoginForm(forms.Form):
    name = forms.CharField(max_length=45, label="",
                           widget=forms.TextInput(attrs={"placeholder":"Username", "class": "form-control"}))
    password = forms.CharField(max_length=45, label="",
                            widget=forms.TextInput(attrs={"placeholder":"Password", "class": "form-control", "type":"password"}))


class ImageUpload(forms.Form):
    image = forms.ImageField(label="",
                             widget=forms.ClearableFileInput(attrs={"accept":"image/*", "multiple":True}))
    description = forms.CharField(max_length=45, label="",
                           widget=forms.TextInput(attrs={"placeholder":"Image Description", "class": "form-control"}))

class AuthorizeForm(forms.Form):
    def __init__(self, n, *args, **kwargs):
        super(AuthorizeForm, self).__init__(*args, **kwargs)
        for i in n:
            self.fields['{}'.format(i.id)] = forms.BooleanField(required=False)


class LikeForm(forms.Form):
    count = forms.Field()

class FilterForm(forms.Form):
    like = forms.BooleanField(required=False)
    date = forms.BooleanField(required=False)