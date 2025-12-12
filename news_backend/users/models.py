from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from functools import cmp_to_key
from articles.models import ArticleBookmark

# Create your models here.

class User(AbstractUser):
    GENDER_CHOICES = [
        ("f", "Female"),
        ("m", "Male"),
        ("o", "Other"),
        ("u", "Unknown")
    ]
    DEFAULT_GENDER_CHOICE = "u"
    country = models.CharField(max_length=100, blank=False, null=True, verbose_name="Ülke Konumu")
    birth_date = models.DateField(null=True, verbose_name="Date of Birth")
    gender = models.CharField(max_length=1, default=DEFAULT_GENDER_CHOICE, choices=GENDER_CHOICES
                              , verbose_name="Gender")
    followers = models.ManyToManyField(to="self", symmetrical=False, blank=True, related_name="following_list")
    bookmarked_articles = models.ManyToManyField(to="articles.Article", blank=True, related_name="bookmarked_by"
                                                 , through="articles.ArticleBookmark")
    viewed_articles = models.ManyToManyField(to="articles.Article", blank=True, related_name="viewed_by"
                                             , through="articles.ArticleView")
    followed_categories = models.ManyToManyField(to="articles.Category", blank=True)
    followed_tags = models.ManyToManyField(to="articles.Tag", blank=True)

    @staticmethod
    def is_username_valid(username):
        # TO DO: implement the method
        pass


    @staticmethod
    def is_password_valid(password):
        # TO DO: implement the method
        pass

    @staticmethod
    def get_sorted_following_or_follower_list(requesting_user, following_or_follower_list):
        if not following_or_follower_list.exists():
            return []
        def compare_followed_users(user1, user2):
            requesting_user_follows_user1 = requesting_user.followers.filter(id=user1.id).exists()
            requesting_user_follows_user2 = requesting_user.followers.filter(id=user2.id).exists()

            if requesting_user_follows_user1 and not requesting_user_follows_user2:
                return -1
            if not requesting_user_follows_user1 and requesting_user_follows_user2:
                return 1

            user1_is_premium = user1.profile.is_premium()
            user2_is_premium = user2.profile.is_premium()

            if user1_is_premium and not user2_is_premium:
                return -1
            if not user1_is_premium and user2_is_premium:
                return 1

            user1_follower_num = user1.followers.count()
            user2_follower_num = user2.followers.count()

            if user1_follower_num > user2_follower_num:
                return -1
            if user2_follower_num > user1_follower_num:
                return 1

            return 0

        return sorted(following_or_follower_list, key=cmp_to_key(compare_followed_users))

    def get_sorted_followed_tags(self):
        return self.followed_tags.order_by("name")

    def get_sorted_followed_categories(self):
        return self.followed_categories.order_by("name")

    def get_sorted_bookmarked_articles(self, newest_first=True):
        TIME_ORDER = "-time" if newest_first else "time"
        sorted_bookmarks = (ArticleBookmark.objects
                            .filter(user=self)
                            .select_related("article")
                            .order_by(TIME_ORDER))
        return [bookmark.article for bookmark in sorted_bookmarks]

    def follows_user(self, user):
        if self == user:
            return False
        return user.followers.filter(id=self.id).exists()







class Author(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name="User")
    slug = models.CharField(max_length=50, unique=True, verbose_name="Slug")
    about = models.TextField(verbose_name="About")
    profile_image = models.ImageField(upload_to="author_profile_images/", blank=True, null=True
                                      , verbose_name="Profile Image")
    articles = models.ManyToManyField(to="articles.Article", blank=True, related_name="authors",
                                      verbose_name="Written Articles")

    def __str__(self):
        return self.user.name

class Editor(models.Model):
    ROLE_CHOICES = [
        ("junior", "Junior"),
        ("senior", "Senior")
    ]

    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name="User")
    slug = models.CharField(max_length=50, unique=True, verbose_name="Slug")
    profile_image = models.ImageField(upload_to="editor_profile_images/", verbose_name="Profile Image")
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, verbose_name="Editor Role")

    def __str__(self):
        return self.user.name

class UserProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="profile")
    biography = models.TextField(blank=True, verbose_name="Biography")
    avatar = models.ImageField(upload_to="user_avatars/", blank=True, null=True, verbose_name="Profile Picture")

    def __str__(self):
        return self.user.name

    def is_premium(self):
        PREMIMUM = "premium"
        return self.user.groups.filter(name=PREMIMUM).exists()

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

    def __str__(self):
        return self.user.name
