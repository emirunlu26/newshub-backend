from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    GENDER_CHOICES = [
        ("f", "Female"),
        ("m", "Male"),
        ("o", "Other"),
    ]
    location = models.CharField(max_length=100, null=True, verbose_name="Ülke Konumu")
    birth_date = models.DateField(auto_now=False, auto_now_add=False, null=True, verbose_name="Date of Birth")
    gender = models.CharField(max_length=1, null=True, choices=GENDER_CHOICES, verbose_name="Gender")
    followers = models.ManyToManyField(to="self", related_name="following_list")
    bookmarked_articles = models.ManyToManyField(to="articles.Article", related_name="bookmarked_by")
    viewed_articles = models.ManyToManyField(to="articles.Article", related_name="viewed_by"
                                             , through="articles.ArticleView")
    followed_categories = models.ManyToManyField(to="articles.Category")
    followed_tags = models.ManyToManyField(to="articles.Tag")

class Author(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name="User")
    slug = models.CharField(max_length=50, unique=True, verbose_name="Slug")
    about = models.TextField(verbose_name="About")
    profile_image = models.FileField(verbose_name="Profile Image")
    articles = models.ManyToManyField(to="articles.Article", verbose_name="Written Articles")

    def __str__(self):
        return self.user.name

class Editor(models.Model):
    ROLE_CHOICES = [
        ("junior", "Junior"),
        ("senior", "Senior")
    ]

    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name="User")
    slug = models.CharField(max_length=50, unique=True, verbose_name="Slug")
    profile_image = models.FileField(verbose_name="Profile Image")
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, verbose_name="Editor Role")

    def __str__(self):
        return self.user.name

class UserProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="profile")
    biography = models.TextField(blank=True, verbose_name="Biography")
    avatar = models.FileField(blank=True, null=True, verbose_name="Profile Picture")

    def __str__(self):
        return self.user.name

class UserCustomization(models.Model):
    THEME_CHOICES = [
        ("dark", "Dark Theme"),
        ("light", "Light Theme")
    ]

    FONT_CHOICES = [
        ("arial", "Arial"),
        ("helvetica", "Helvetica"),
        ("verdana", "Verdana"),
        ("roboto", "Roboto")
    ]

    FONT_COLOUR_CHOICES = [
        ("#FFFFFF", "White"),
        ("#000000", "Black"),
        ("#FF0000", "Red"),
        ("#00FF00", "Green"),
        ("#0000FF", "Blue")
    ]

    DEFAULT_THEME = "dark"
    DEFAULT_FONT_TYPE = "arial"
    DEFAULT_FONT_SIZE = 14
    DEFAULT_FONT_COLOUR = "#FFFFFF"

    def validate_font_size(self, font_size):
        MIN_FONT_SIZE = 1
        MAX_FONT_SIZE = 72
        if font_size < MIN_FONT_SIZE or font_size > MAX_FONT_SIZE:
            return ValidationError(
                message=f"Font size out of range(min:{MIN_FONT_SIZE}, max:{MAX_FONT_SIZE})"
            )


    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="customization")
    theme = models.CharField(max_length=50, choices=THEME_CHOICES, default=DEFAULT_THEME, verbose_name="Theme")
    font_type = models.CharField(max_length=50, choices=FONT_CHOICES, default=DEFAULT_FONT_TYPE
                                 , verbose_name="Font Type")
    font_size = models.IntegerField(default=DEFAULT_FONT_SIZE, validators=[validate_font_size]
                                    , verbose_name="Font Size")
    font_colour = models.CharField(max_length=50, choices=FONT_COLOUR_CHOICES, default=DEFAULT_FONT_COLOUR
                                   , verbose_name="Font Colour")

    def is_premium(self):
        # TO DO: check if the user belongs to the group of premium users
        pass

    def __str__(self):
        return self.user.name
