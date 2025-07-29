from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import GreenProduct, EcoEvent, BlogPost, UserProfile, Submission, GreenTip, Partner, Project, Feedback, NewsletterSignup, Brand, SecurityQuestion
from .forms import GreenProductForm, EcoEventForm, BlogPostForm, UserProfileForm, SubmissionForm, GreenTipForm, PartnerForm, ProjectForm, FeedbackForm, NewsletterSignupForm, SearchForm, CustomLoginForm, CustomRegisterForm, UsernameForm, SecurityQuestionForm, SetNewPasswordForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.views.generic.edit import FormView
from django.contrib import messages
from django.conf import settings
from .models import Brand, GreenProduct
from django.utils import timezone
import datetime
from django.urls import reverse
from django.contrib.auth.models import User
import random
import smtplib
from django.conf import settings
from django.core.mail import send_mail
from django.conf import settings
from django.db import models

# Create your views here.

def home(request):
    import datetime
    today = str(datetime.date.today())
    visit_history = request.session.get('visit_history', {})
    visit_history[today] = visit_history.get(today, 0) + 1
    request.session['visit_history'] = visit_history
    visits_today = visit_history[today]
    total_visits = sum(visit_history.values())
    response = render(request, 'greentech/home.html', {'user': request.user})
    response.set_cookie('visits_today', visits_today)
    response.set_cookie('total_visits', total_visits)
    return response

class GreenProductListView(ListView):
    model = GreenProduct
    template_name = 'greentech/greenproduct_list.html'
    context_object_name = 'products'

    def get(self, request, *args, **kwargs):
        # Track visits
        import datetime
        today = str(datetime.date.today())
        last_visit = request.session.get('last_visit')
        visits_today = request.session.get('visits_today', 0)
        total_visits = request.session.get('total_visits', 0)
        if last_visit == today:
            visits_today += 1
        else:
            visits_today = 1
        total_visits += 1
        request.session['last_visit'] = today
        request.session['visits_today'] = visits_today
        request.session['total_visits'] = total_visits
        return super().get(request, *args, **kwargs)

class GreenProductDetailView(DetailView):
    model = GreenProduct
    template_name = 'greentech/greenproduct_detail.html'
    context_object_name = 'product'

class EcoEventListView(ListView):
    model = EcoEvent
    template_name = 'greentech/event_list.html'
    context_object_name = 'events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Track visits
        import datetime
        today = str(datetime.date.today())
        visit_history = self.request.session.get('visit_history', {})
        visit_history[today] = visit_history.get(today, 0) + 1
        self.request.session['visit_history'] = visit_history
        
        return context

class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'greentech/blog_list.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Track visits
        import datetime
        today = str(datetime.date.today())
        visit_history = self.request.session.get('visit_history', {})
        visit_history[today] = visit_history.get(today, 0) + 1
        self.request.session['visit_history'] = visit_history
        
        return context

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'greentech/blog_detail.html'
    context_object_name = 'post'

class AboutView(TemplateView):
    template_name = 'greentech/about.html'

class ContactView(TemplateView):
    template_name = 'greentech/contact.html'

class TeamView(TemplateView):
    template_name = 'greentech/team.html'

class BrandListView(ListView):
    model = Brand
    template_name = 'greentech/brand_list.html'
    context_object_name = 'brands'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            from .models import FavoriteBrand
            wishlisted_ids = set(FavoriteBrand.objects.filter(user=self.request.user).values_list('brand_id', flat=True))
        else:
            wishlisted_ids = set()
        context['wishlisted_ids'] = wishlisted_ids
        
        # Track visits
        import datetime
        today = str(datetime.date.today())
        visit_history = self.request.session.get('visit_history', {})
        visit_history[today] = visit_history.get(today, 0) + 1
        self.request.session['visit_history'] = visit_history
        
        return context

def submission_success(request):
    return render(request, 'greentech/submission_success.html')

@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    response = render(request, 'greentech/profile.html', {
        'user': request.user,
        'profile': profile,
    })
    return response

@login_required
def user_history(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    visit_history = request.session.get('visit_history', {})
    visits_today = visit_history.get(str(datetime.date.today()), 0)
    total_visits = sum(visit_history.values())
    return render(request, 'greentech/user_history.html', {
        'user': request.user,
        'profile': profile,
        'visits_today': visits_today,
        'total_visits': total_visits,
        'visit_history': visit_history,
    })

@login_required
def user_dashboard(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Get visit statistics from UserVisit model
    from .models import UserVisit
    from django.utils import timezone
    from datetime import timedelta
    
    today = timezone.now().date()
    
    # Get visits for today
    visits_today = UserVisit.objects.filter(
        user=request.user, 
        login_date=today
    ).count()
    
    # Get total visits
    total_visits = UserVisit.objects.filter(user=request.user).count()
    
    # Get last 7 days visits
    last_7_days = UserVisit.objects.filter(
        user=request.user,
        login_date__gte=today - timedelta(days=7)
    ).count()
    
    # Get most active day
    most_active_day = UserVisit.objects.filter(user=request.user).values('login_date').annotate(
        visit_count=models.Count('id')
    ).order_by('-visit_count').first()
    
    most_visits = most_active_day['visit_count'] if most_active_day else 0
    most_active_date = most_active_day['login_date'] if most_active_day else None
    
    # Get first visit date
    first_visit = UserVisit.objects.filter(user=request.user).order_by('login_date').first()
    days_since_first_visit = (today - first_visit.login_date).days if first_visit else 0
    
    # Get recent visit dates (last 10)
    recent_visits = UserVisit.objects.filter(user=request.user).values('login_date').annotate(
        visit_count=models.Count('id')
    ).order_by('-login_date')[:10]
    
    num_orders = 0  # Replace with actual order count if you have an Order model
    active_duration = (timezone.now().date() - request.user.date_joined.date()).days
    from .models import FavoriteBrand
    favorite_brands = [fb.brand for fb in FavoriteBrand.objects.filter(user=request.user).select_related('brand')]
    
    return render(request, 'greentech/user_dashboard.html', {
        'user': request.user,
        'profile': profile,
        'visits_today': visits_today,
        'total_visits': total_visits,
        'last_7_days_visits': last_7_days,
        'most_active_day': most_active_date,
        'most_visits': most_visits,
        'days_since_first_visit': days_since_first_visit,
        'recent_visits': recent_visits,
        'num_orders': num_orders,
        'active_duration': active_duration,
        'favorite_brands': favorite_brands,
    })

# Update SubmissionCreateView to redirect to submission_success
class SubmissionCreateView(CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name = 'greentech/submission_form.html'
    success_url = reverse_lazy('submission-success')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class UserProfileUpdateView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'greentech/profile_form.html'
    success_url = reverse_lazy('profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        return UserProfile.objects.get(user=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        # Ensure the user profile is updated and redirect to profile
        return response

class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = 'greentech/login.html'

    def form_valid(self, form):
        from django.contrib import messages
        user = form.get_user()
        
        # Record the visit when user logs in
        from .models import UserVisit
        UserVisit.record_visit(user, self.request.session.session_key)
        
        messages.success(self.request, f'🎉 Welcome back, {user.first_name}! You have successfully logged in.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        from django.contrib import messages
        # Handle specific login errors
        if 'username' in form.errors or 'password' in form.errors:
            messages.error(self.request, '❌ Invalid username or password. Please check your credentials and try again.')
        else:
            messages.error(self.request, '❌ Login failed. Please try again.')
        return super().form_invalid(form)

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')

class RegisterView(FormView):
    template_name = 'greentech/register.html'
    form_class = CustomRegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        try:
            # Check if username already exists
            username = form.cleaned_data.get('username')
            if User.objects.filter(username=username).exists():
                messages.error(self.request, f'Username "{username}" is already taken. Please choose a different username.')
                return self.form_invalid(form)
            
            # Check if email already exists
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                messages.error(self.request, f'Email "{email}" is already registered. Please use a different email or try logging in.')
                return self.form_invalid(form)
            
            # Save the user
            user = form.save()
            
            # Success message with user details
            messages.success(
                self.request, 
                f'🎉 Registration successful! Welcome to GreenTech, {user.first_name}! '
                f'Your account has been created with username: {user.username}. '
                f'You can now log in with your credentials.'
            )
            
            return super().form_valid(form)
            
        except Exception as e:
            # Handle any unexpected errors
            messages.error(
                self.request, 
                f'❌ Registration failed due to an unexpected error. Please try again. '
                f'If the problem persists, contact support.'
            )
            return self.form_invalid(form)

    def form_invalid(self, form):
        # Handle specific form validation errors
        for field, errors in form.errors.items():
            for error in errors:
                if field == 'username':
                    if 'unique' in error.lower():
                        messages.error(self.request, 'Username is already taken. Please choose a different username.')
                    else:
                        messages.error(self.request, f'Username error: {error}')
                elif field == 'email':
                    if 'unique' in error.lower():
                        messages.error(self.request, 'Email is already registered. Please use a different email.')
                    elif 'invalid' in error.lower():
                        messages.error(self.request, 'Please enter a valid email address.')
                    else:
                        messages.error(self.request, f'Email error: {error}')
                elif field == 'password1':
                    if 'too short' in error.lower():
                        messages.error(self.request, 'Password must be at least 8 characters long.')
                    elif 'too common' in error.lower():
                        messages.error(self.request, 'Password is too common. Please choose a stronger password.')
                    elif 'numeric' in error.lower():
                        messages.error(self.request, 'Password cannot be entirely numeric.')
                    else:
                        messages.error(self.request, f'Password error: {error}')
                elif field == 'password2':
                    if 'mismatch' in error.lower():
                        messages.error(self.request, 'Passwords do not match. Please enter the same password in both fields.')
                    else:
                        messages.error(self.request, f'Password confirmation error: {error}')
                elif field == 'security_question_1' or field == 'security_question_2':
                    if 'required' in error.lower():
                        messages.error(self.request, f'Please select a security question for {field.replace("_", " ").title()}.')
                    else:
                        messages.error(self.request, f'Security question error: {error}')
                elif field == 'security_answer_1' or field == 'security_answer_2':
                    if 'required' in error.lower():
                        messages.error(self.request, f'Please provide an answer for {field.replace("_", " ").title()}.')
                    else:
                        messages.error(self.request, f'Security answer error: {error}')
                elif field == '__all__':
                    if 'different' in error.lower():
                        messages.error(self.request, 'Please select different security questions for question 1 and question 2.')
                    else:
                        messages.error(self.request, f'Form error: {error}')
                else:
                    messages.error(self.request, f'{field.title()} error: {error}')
        
        return super().form_invalid(form)

class CustomPasswordResetView(PasswordResetView):
    template_name = 'greentech/password_reset.html'
    email_template_name = 'greentech/password_reset_email.html'
    subject_template_name = 'greentech/password_reset_subject.txt'
    success_url = reverse_lazy('login')

def search(request):
    filter_type = request.GET.get('filter', 'brand')
    query = request.GET.get('query', '').strip()
    results = []
    
    if query:
        from .models import Brand, GreenProduct
        if filter_type == 'brand':
            # Show GreenProducts for the selected brand
            results = GreenProduct.objects.filter(brand__name__icontains=query).select_related('brand')
        elif filter_type == 'category':
            # Show products in the selected category
            results = GreenProduct.objects.filter(category__icontains=query).select_related('brand')
    
    return render(request, 'greentech/search_results.html', {
        'results': results, 
        'filter': filter_type, 
        'query': query,
        'total_results': len(results)
    })

# Add a context processor for brands and categories

def brands_and_categories(request):
    brands = Brand.objects.all().order_by('name')
    categories = GreenProduct.objects.values_list('category', flat=True).distinct().order_by('category')
    return {'all_brands': brands, 'all_categories': categories}

@login_required
def add_to_wishlist(request, brand_id):
    from .models import Brand, FavoriteBrand
    brand = Brand.objects.get(id=brand_id)
    FavoriteBrand.objects.get_or_create(user=request.user, brand=brand)
    return redirect('brand-list')

@login_required
def remove_from_wishlist(request, brand_id):
    from .models import Brand, FavoriteBrand
    brand = Brand.objects.get(id=brand_id)
    FavoriteBrand.objects.filter(user=request.user, brand=brand).delete()
    return redirect('brand-list')

@login_required
def view_brand(request, brand_id):
    brand = Brand.objects.get(id=brand_id)
    # Track recently viewed brands in session
    recently_viewed = request.session.get('recently_viewed_brands', [])
    if brand_id in recently_viewed:
        recently_viewed.remove(brand_id)
    recently_viewed.insert(0, brand_id)
    recently_viewed = recently_viewed[:10]  # Keep only last 10
    request.session['recently_viewed_brands'] = recently_viewed
    return render(request, 'greentech/brand_detail.html', {'brand': brand})

@login_required
def history(request):
    brand_ids = request.session.get('recently_viewed_brands', [])
    brands = Brand.objects.filter(id__in=brand_ids)
    # Preserve order
    brands = sorted(brands, key=lambda b: brand_ids.index(b.id))
    return render(request, 'greentech/history.html', {'brands': brands})

def forgot_password_view(request):
    if request.method == 'POST':
        form = UsernameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = User.objects.get(username=username)
                # Check if user has security questions set up
                security_questions = SecurityQuestion.objects.filter(user=user)
                if security_questions.exists():
                    # Randomly select one of the two questions
                    selected_question = random.choice(security_questions)
                    request.session['reset_username'] = username
                    request.session['security_question_id'] = selected_question.id
                    request.session['security_question'] = selected_question.question
                    return redirect('security_question')
                else:
                    messages.error(request, 'No security questions found for this user. Please contact support.')
            except User.DoesNotExist:
                messages.error(request, 'Username not found.')
    else:
        form = UsernameForm()
    
    return render(request, 'greentech/forgot_password.html', {'form': form})

def security_question_view(request):
    username = request.session.get('reset_username')
    question_id = request.session.get('security_question_id')
    
    if not username or not question_id:
        messages.error(request, 'Please enter your username first.')
        return redirect('forgot_password')
    
    try:
        user = User.objects.get(username=username)
        security_question = SecurityQuestion.objects.get(id=question_id, user=user)
    except (User.DoesNotExist, SecurityQuestion.DoesNotExist):
        messages.error(request, 'User or security question not found.')
        return redirect('forgot_password')
    
    if request.method == 'POST':
        form = SecurityQuestionForm(request.POST)
        if form.is_valid():
            answer = form.cleaned_data['answer']
            if security_question.check_answer(answer):
                messages.success(request, 'Security question answered correctly! Please set your new password.')
                return redirect('reset_password')
            else:
                messages.error(request, 'Incorrect answer. Please try again.')
    else:
        form = SecurityQuestionForm()
    
    return render(request, 'greentech/security_question.html', {
        'form': form, 
        'question': security_question.question,
        'username': username
    })

def reset_password_view(request):
    username = request.session.get('reset_username')
    if not username:
        messages.error(request, 'Please complete the security verification first.')
        return redirect('forgot_password')
    
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('forgot_password')
    
    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            user.set_password(new_password)
            user.save()
            
            # Clear session data
            if 'reset_username' in request.session:
                del request.session['reset_username']
            if 'security_question' in request.session:
                del request.session['security_question']
            
            messages.success(request, 'Password reset successful! You can now login with your new password.')
            return redirect('login')
    else:
        form = SetNewPasswordForm()
    
    return render(request, 'greentech/reset_password.html', {'form': form})

def newsletter_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Check if email already exists
            from .models import NewsletterSignup
            newsletter, created = NewsletterSignup.objects.get_or_create(email=email)
            if created:
                messages.success(request, 'Thank you for subscribing to our newsletter!')
            else:
                messages.info(request, 'You are already subscribed to our newsletter.')
        else:
            messages.error(request, 'Please provide a valid email address.')
    
    return redirect('home')
