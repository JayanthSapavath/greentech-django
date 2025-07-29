#  GreenTech - Sustainable Fashion Platform

A comprehensive Django-based e-commerce platform dedicated to promoting sustainable fashion and ethical practices in the clothing industry.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

##  Overview

GreenTech is a curated platform that brings together sustainable fashion brands and conscious consumers. Our mission is to promote ethical fashion choices while providing a seamless shopping experience for eco-friendly clothing and accessories.

###  Mission
To transform the fashion industry through sustainable practices, ethical production, and innovative technology solutions.

### Vision (2030)
- Connect 1,000+ sustainable brands with 10 million+ conscious consumers
- Achieve 100% circular fashion practices
- Create a global community of 5 million+ sustainability advocates
- Influence 25% of global fashion purchases to be sustainable

## Features

### E-commerce Features
- **Brand Showcase**: Curated collection of sustainable fashion brands
- **Product Catalog**: Detailed product listings with sustainability metrics
- **Search & Filter**: Advanced search by category, brand, and sustainability criteria
- **User Accounts**: Personalized user profiles and dashboards
- **Wishlist**: Save favorite brands and products
- **Visit Tracking**: Login-based visit statistics and analytics

### Authentication & Security
- **User Registration**: Secure account creation with email validation
- **Login System**: Custom authentication with visit tracking
- **Password Reset**: Security question-based password recovery
- **Profile Management**: User profile customization and settings
- **Session Management**: Secure session handling with timeout features

### Dashboard & Analytics
- **User Dashboard**: Personalized statistics and activity tracking
- **Visit Analytics**: Login-based visit counting and reporting
- **Recent Activity**: User activity history and engagement metrics
- **Profile Statistics**: User profile insights and preferences

###  User Interface
- **Responsive Design**: Mobile-first, Bootstrap-powered interface
- **Modern UI**: Clean, professional design with sustainable theme
- **Accessibility**: WCAG compliant design patterns
- **Cross-browser**: Compatible with all modern browsers

###  Content Management
- **Events System**: Sustainable fashion events and workshops
- **Blog Platform**: Content management for sustainability articles
- **Newsletter**: Email subscription system
- **Team Showcase**: Team member profiles and roles

##  Technology Stack

### Backend
- **Django 4.x**: Web framework
- **Python 3.x**: Programming language
- **SQLite**: Database (development)
- **Django ORM**: Database abstraction layer

### Frontend
- **Bootstrap 5.3.0**: CSS framework
- **Bootstrap Icons**: Icon library
- **HTML5/CSS3**: Markup and styling
- **JavaScript**: Interactive features

### Development Tools
- **Git**: Version control
- **Django Admin**: Content management
- **Django Forms**: Form handling and validation
- **Django Messages**: User notifications

##  Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/GreenTechProject.git
   cd GreenTechProject
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Load initial data**
   ```bash
   python manage.py loaddata greentech/fixtures/brands.json
   python manage.py loaddata greentech/fixtures/initial_data.json
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Usage

### For Users
1. **Browse Brands**: Explore sustainable fashion brands
2. **Search Products**: Use category-based search functionality
3. **Create Account**: Register for personalized experience
4. **Track Activity**: Monitor your sustainable fashion journey
5. **Stay Updated**: Subscribe to newsletter for latest updates

### For Administrators
1. **Manage Content**: Use Django admin for content management
2. **Monitor Analytics**: Track user engagement and platform usage
3. **Update Events**: Add and manage sustainable fashion events
4. **Brand Management**: Curate and update brand information

## 📁 Project Structure

```
GreenTechProject/
├── GreenTechProject/          # Django project settings
│   ├── __init__.py
│   ├── settings.py           # Project configuration
│   ├── urls.py              # Main URL routing
│   ├── asgi.py              # ASGI configuration
│   └── wsgi.py              # WSGI configuration
├── greentech/               # Main application
│   ├── __init__.py
│   ├── admin.py             # Admin interface configuration
│   ├── apps.py              # App configuration
│   ├── forms.py             # Form definitions
│   ├── models.py            # Database models
│   ├── urls.py              # App URL routing
│   ├── views.py             # View functions and classes
│   ├── tests.py             # Test cases
│   ├── fixtures/            # Initial data
│   │   ├── brands.json      # Brand data
│   │   └── initial_data.json # Product data
│   └── templatetags/        # Custom template tags
├── templates/               # HTML templates
│   └── greentech/          # App-specific templates
│       ├── base.html       # Base template
│       ├── home.html       # Homepage
│       ├── about.html      # About page
│       ├── team.html       # Team page
│       ├── login.html      # Login form
│       ├── register.html   # Registration form
│       ├── profile.html    # User profile
│       ├── dashboard.html  # User dashboard
│       ├── brand_list.html # Brand listing
│       ├── event_list.html # Events listing
│       └── search_results.html # Search results
├── static/                  # Static files
│   ├── style.css           # Custom CSS
│   ├── about.jpg           # Images
│   ├── hero.jpg
│   └── other images...
├── media/                   # User-uploaded files
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── .gitignore             # Git ignore rules
└── db.sqlite3             # Database file
```

##  API Endpoints

### Authentication
- `POST /login/` - User login
- `POST /logout/` - User logout
- `POST /register/` - User registration
- `GET /profile/` - User profile
- `POST /forgot-password/` - Password reset request

### Content
- `GET /` - Homepage
- `GET /brands/` - Brand listing
- `GET /events/` - Events listing
- `GET /blog/` - Blog posts
- `GET /about/` - About page
- `GET /team/` - Team page

### User Features
- `GET /dashboard/` - User dashboard
- `GET /search/` - Search functionality
- `POST /newsletter/` - Newsletter subscription
- `POST /brands/<id>/wishlist/add/` - Add to wishlist
- `POST /brands/<id>/wishlist/remove/` - Remove from wishlist

##  Design Features

### Color Scheme
- **Primary**: Charcoal (#36454f)
- **Secondary**: Sky Blue (#0ea5e9)
- **Accent**: Yellow (#ffc107)
- **Background**: Light Grey (#f4f7f6)

### Responsive Design
- **Mobile-first** approach
- **Bootstrap 5** grid system
- **Cross-device** compatibility
- **Touch-friendly** interface

## 🔒 Security Features

- **CSRF Protection**: Built-in Django CSRF tokens
- **Session Security**: Secure session management
- **Password Hashing**: Django's secure password hashing
- **Input Validation**: Form validation and sanitization
- **SQL Injection Protection**: Django ORM protection

##  Database Models

### Core Models
- **User**: Extended user model with profiles
- **Brand**: Sustainable fashion brands
- **GreenProduct**: Products with sustainability metrics
- **EcoEvent**: Sustainable fashion events
- **BlogPost**: Content management
- **UserVisit**: Visit tracking and analytics
- **SecurityQuestion**: Password reset security

### Relationship Models
- **FavoriteBrand**: User-brand relationships
- **UserProfile**: Extended user information
- **NewsletterSignup**: Email subscriptions

##  Deployment

### Production Setup
1. **Environment Variables**: Configure production settings
2. **Database**: Set up PostgreSQL or MySQL
3. **Static Files**: Configure static file serving
4. **Media Files**: Set up media file storage
5. **Web Server**: Configure Nginx/Apache
6. **WSGI**: Set up Gunicorn/uWSGI

### Recommended Hosting
- **Heroku**: Easy deployment with PostgreSQL
- **DigitalOcean**: VPS with full control
- **AWS**: Scalable cloud infrastructure
- **Railway**: Modern deployment platform

##  Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Development Guidelines
- Follow PEP 8 Python style guide
- Write comprehensive tests
- Update documentation
- Use meaningful commit messages

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Team

- **Amith Vinayaka** 
- **Jayanth Sapavath** 
- **Lovedeep Singh** 
- **Mahzabin Chowdhury** 
- **Rajat Yadav** 

##  Contact

- **Website**: [GreenTech Platform](http://127.0.0.1:8000/)
- **Email**: contact@greentech.com
- **GitHub**: [@yourusername](https://github.com/yourusername)

##  Acknowledgments

- Django community for the excellent framework
- Bootstrap team for the responsive design system
- Unsplash for high-quality images
- All sustainable fashion brands featured on the platform

---
