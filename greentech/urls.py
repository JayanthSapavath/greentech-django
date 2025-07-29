from django.urls import path
from . import views
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', RedirectView.as_view(url='/brands/', permanent=False)),
    path('products/<int:pk>/', views.GreenProductDetailView.as_view(), name='product-detail'),
    path('events/', views.EcoEventListView.as_view(), name='event-list'),
    path('blog/', views.BlogPostListView.as_view(), name='blog-list'),
    path('blog/<int:pk>/', views.BlogPostDetailView.as_view(), name='blog-detail'),
    path('submit/', views.SubmissionCreateView.as_view(), name='submission'),
    path('submission-success/', views.submission_success, name='submission-success'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.UserProfileUpdateView.as_view(), name='profile-edit'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('search/', views.search, name='search'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('team/', views.TeamView.as_view(), name='team'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('security-question/', views.security_question_view, name='security_question'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='greentech/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='greentech/password_reset_complete.html'), name='password_reset_complete'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='greentech/password_reset_done.html'), name='password_reset_done'),
    path('brands/', views.BrandListView.as_view(), name='brand-list'),
    path('brands/<int:brand_id>/wishlist/add/', views.add_to_wishlist, name='add-to-wishlist'),
    path('brands/<int:brand_id>/wishlist/remove/', views.remove_from_wishlist, name='remove-from-wishlist'),
    path('brands/<int:brand_id>/', views.view_brand, name='brand-detail'),
    path('history/', views.history, name='history'),
    path('accounts/profile/', RedirectView.as_view(url='/profile/', permanent=False)),
    path('dashboard/', views.user_dashboard, name='user-dashboard'),
    path('newsletter/', views.newsletter_signup, name='newsletter'),
] 