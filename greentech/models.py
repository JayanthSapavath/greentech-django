from django.db import models

# Create your models here.

class GreenProduct(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name

class EcoEvent(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    location = models.CharField(max_length=100)
    description = models.TextField()

class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    country = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=20, blank=True)

class Submission(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    description = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

class GreenTip(models.Model):
    tip = models.CharField(max_length=255)
    source = models.CharField(max_length=100, blank=True)

class Partner(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='partners/', blank=True, null=True)

class Project(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

class Feedback(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class NewsletterSignup(models.Model):
    email = models.EmailField(unique=True)
    date_signed_up = models.DateTimeField(auto_now_add=True)

class Brand(models.Model):
    name = models.CharField(max_length=100)
    logo_url = models.URLField()
    website_url = models.URLField()
    description = models.TextField(blank=True)
    card_image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class FavoriteBrand(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='favorite_brands')
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'brand')

class PasswordResetCode(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Reset code for {self.user.email}"

    def is_expired(self):
        from django.utils import timezone
        from datetime import timedelta
        return self.created_at < timezone.now() - timedelta(minutes=10)

class SecurityQuestion(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    question_number = models.IntegerField(default=1)  # 1 or 2 to identify which question
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'question_number']  # Each user can have only one question per number
    
    def __str__(self):
        return f"Security question {self.question_number} for {self.user.username}"
    
    def check_answer(self, user_answer):
        """Check if the provided answer matches (case-insensitive)"""
        return self.answer.lower().strip() == user_answer.lower().strip()

class UserVisit(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    login_date = models.DateField(auto_now_add=True)
    login_time = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    
    class Meta:
        ordering = ['-login_time']
        unique_together = ['user', 'login_date', 'session_key']  # One visit per user per day per session
    
    def __str__(self):
        return f"{self.user.username} - {self.login_date}"
    
    @classmethod
    def record_visit(cls, user, session_key=None):
        """Record a new visit for the user"""
        from django.utils import timezone
        today = timezone.now().date()
        visit, created = cls.objects.get_or_create(
            user=user,
            login_date=today,
            session_key=session_key,
            defaults={'login_time': timezone.now()}
        )
        return visit, created
