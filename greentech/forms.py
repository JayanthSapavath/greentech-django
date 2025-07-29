from django import forms
from .models import GreenProduct, EcoEvent, BlogPost, UserProfile, Submission, GreenTip, Partner, Project, Feedback, NewsletterSignup
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class GreenProductForm(forms.ModelForm):
    class Meta:
        model = GreenProduct
        fields = '__all__'

class EcoEventForm(forms.ModelForm):
    class Meta:
        model = EcoEvent
        fields = '__all__'

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = '__all__'

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=True, label='First Name')
    email = forms.EmailField(required=True, label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(required=True, label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(required=False, label='Country', widget=forms.TextInput(attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], required=False, label='Gender', widget=forms.Select(attrs={'class': 'form-select'}))
    avatar = forms.ImageField(label='Profile Picture', required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    bio = forms.CharField(label='Bio / Interests', required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))

    class Meta:
        model = UserProfile
        fields = ['first_name', 'username', 'email', 'avatar', 'country', 'gender', 'bio']
        labels = {
            'avatar': 'Profile Picture',
            'bio': 'Bio / Interests',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['email'].initial = user.email
            self.fields['username'].initial = user.username
            if hasattr(user, 'userprofile'):
                self.fields['country'].initial = user.userprofile.country
                self.fields['gender'].initial = user.userprofile.gender

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        profile.country = self.cleaned_data.get('country', '')
        profile.gender = self.cleaned_data.get('gender', '')
        if commit:
            user.save()
            profile.save()
        return profile

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file', 'description']

class GreenTipForm(forms.ModelForm):
    class Meta:
        model = GreenTip
        fields = '__all__'

class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = '__all__'

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']

class NewsletterSignupForm(forms.ModelForm):
    class Meta:
        model = NewsletterSignup
        fields = ['email']

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label='Search')
    category = forms.ChoiceField(choices=[('products', 'Products'), ('events', 'Events'), ('blog', 'Blog')], required=False)

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class CustomRegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True, label='First Name')
    email = forms.EmailField(required=True)
    country = forms.CharField(required=True)
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], required=True)
    
    # Security Questions for Password Reset
    security_question_1 = forms.ChoiceField(
        choices=[
            ('', 'Select a security question'),
            ('What was your first pet\'s name?', 'What was your first pet\'s name?'),
            ('In which city were you born?', 'In which city were you born?'),
            ('What is your mother\'s maiden name?', 'What is your mother\'s maiden name?'),
            ('What was the name of your first school?', 'What was the name of your first school?'),
            ('What is your favorite color?', 'What is your favorite color?'),
            ('What is the name of your childhood best friend?', 'What is the name of your childhood best friend?'),
            ('What is your favorite movie?', 'What is your favorite movie?'),
            ('What is the name of the street you grew up on?', 'What is the name of the street you grew up on?'),
        ],
        required=True,
        label='Security Question 1'
    )
    security_answer_1 = forms.CharField(
        required=True,
        label='Answer to Question 1',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your answer'})
    )
    
    security_question_2 = forms.ChoiceField(
        choices=[
            ('', 'Select a security question'),
            ('What was your first pet\'s name?', 'What was your first pet\'s name?'),
            ('In which city were you born?', 'In which city were you born?'),
            ('What is your mother\'s maiden name?', 'What is your mother\'s maiden name?'),
            ('What was the name of your first school?', 'What was the name of your first school?'),
            ('What is your favorite color?', 'What is your favorite color?'),
            ('What is the name of your childhood best friend?', 'What is the name of your childhood best friend?'),
            ('What is your favorite movie?', 'What is your favorite movie?'),
            ('What is the name of the street you grew up on?', 'What is the name of the street you grew up on?'),
        ],
        required=True,
        label='Security Question 2'
    )
    security_answer_2 = forms.CharField(
        required=True,
        label='Answer to Question 2',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your answer'})
    )

    class Meta:
        model = User
        fields = ("first_name", "username", "email", "password1", "password2", "country", "gender", "security_question_1", "security_answer_1", "security_question_2", "security_answer_2")

    def clean(self):
        cleaned_data = super().clean()
        question1 = cleaned_data.get('security_question_1')
        question2 = cleaned_data.get('security_question_2')
        
        # Check if both questions are different
        if question1 and question2 and question1 == question2:
            raise forms.ValidationError("Please select different security questions.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        if commit:
            user.save()
            # Save extra fields to UserProfile
            from .models import UserProfile
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.country = self.cleaned_data["country"]
            profile.gender = self.cleaned_data["gender"]
            profile.save()
            
            # Save security questions
            from .models import SecurityQuestion
            # Save first security question
            SecurityQuestion.objects.create(
                user=user,
                question=self.cleaned_data["security_question_1"],
                answer=self.cleaned_data["security_answer_1"],
                question_number=1
            )
            # Save second security question
            SecurityQuestion.objects.create(
                user=user,
                question=self.cleaned_data["security_question_2"],
                answer=self.cleaned_data["security_answer_2"],
                question_number=2
            )
        return user 

class EmailForm(forms.Form):
    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )

class OTPForm(forms.Form):
    otp = forms.CharField(
        label='Verification Code',
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter 6-digit code',
            'maxlength': '6',
            'pattern': '[0-9]{6}'
        })
    )

class SetPasswordForm(forms.Form):
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password'
        })
    )
    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')
        
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords don't match")
            if len(password1) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long")
        
        return cleaned_data 

class UsernameForm(forms.Form):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your username'
        })
    )

class SecurityQuestionForm(forms.Form):
    answer = forms.CharField(
        label='Answer',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your answer'
        })
    )

class SetNewPasswordForm(forms.Form):
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password'
        })
    )
    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')
        
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords don't match")
            if len(password1) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long")
        
        return cleaned_data 