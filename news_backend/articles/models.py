from ckeditor.fields import RichTextField
from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Name")
    slug = models.CharField(max_length=50, unique=True, verbose_name="Slug")
    parent_category = models.ForeignKey(to="articles.Category", on_delete=models.CASCADE
                                        , verbose_name="Parent Category")
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name="Name")
    slug = models.CharField(max_length=50, unique=True, verbose_name="Slug")

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Name")
    slug = models.CharField(max_length=100, unique=True, verbose_name="Slug")

    def __str__(self):
        return self.name


class Article(models.Model):
    ARTICLE_TYPE_CHOICES = [
        ("news", "News Article"),
        ("opinion", "Opinion"),
        ("column", "Column"),
        ("analysis", "Analysis")
    ]

    ARTICLE_STATUS_CHOICES = [
        ("d-in-progress", "Draft In Progress"),
        ("d-completed", "Draft Completed"),
        ("in-review", "In Review"),
        ("published", "Published")
    ]

    DEFAULT_ARTICLE_STATUS = "d-in-progress"

    type = models.CharField(max_length=50, choices=ARTICLE_TYPE_CHOICES, verbose_name="Article Type")
    slug = models.CharField(max_length=100, unique=True, verbose_name="Slug")
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="Writing Time")
    published_at = models.DateTimeField(auto_now=False, auto_created=False, verbose_name="Publication Time")
    editors = models.ManyToManyField(to="users.Editor", verbose_name="Editor")
    title = models.CharField(max_length=255, verbose_name="Title")
    content = RichTextField()
    summary = models.TextField(verbose_name="Summary")
    status = models.CharField(max_length=50, choices=ARTICLE_STATUS_CHOICES
                              , default=DEFAULT_ARTICLE_STATUS, verbose_name="Status")
    cover_image = models.FileField(verbose_name="Cover Image")
    requires_premium = models.BooleanField(default=False, verbose_name="Requires Premium")
    tags = models.ManyToManyField(to=Tag, verbose_name="Tag")
    categories = models.ManyToManyField(to=Category, verbose_name="Category")
    regions = models.ManyToManyField(to="articles.Region", verbose_name="Region")

    def __str__(self):
        return self.title

class ArticleView(models.Model):
    user = models.ForeignKey(to="users.User", on_delete=models.CASCADE, verbose_name="Viewing User")
    article = models.ForeignKey(to=Article, on_delete= models.CASCADE, verbose_name="Viewed Article")
    time = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name="View Time")
    duration_seconds = models.IntegerField(verbose_name="View Duration In Seconds")

class ArticleReaction(models.Model):
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE, related_name="reactions"
                                , verbose_name="Reacted Article")
    reaction = models.ForeignKey(to="posts.Reaction", on_delete=models.CASCADE, verbose_name="Reaction")
    reaction_owner = models.ForeignKey(to="users.User", on_delete=models.CASCADE, related_name="article_reactions"
                              , verbose_name="Reacting User")

    def __str__(self):
        return (f"Article: {self.article.name}\n"
                f"Reaction: {self.reaction.name}\n"
                f"Owner: {self.reaction_owner.name}")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ["article", "reaction_owner"],
                name="unique_user_reaction_per_article"
            )
        ]

class EditTask(models.Model):
    title = models.CharField(max_length=255, verbose_name="Task Title")
    description = models.TextField(verbose_name="Task Description")
    edited_article = models.ForeignKey(to=Article,on_delete=models.CASCADE, related_name="edit_tasks"
                                       , verbose_name="Edited Article")
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="Edit Creation Time")
    deadline = models.DateField(auto_now=False, auto_now_add=False, verbose_name="Deadline")
    completed_at = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name="Completion Time")
    created_by = models.ForeignKey(to="users.Editor", on_delete=models.CASCADE, related_name="created_tasks"
                                   , verbose_name="Task Creator Editor")
    assigned_editor = models.ForeignKey(to="users.Editor", on_delete=models.CASCADE, related_name="assigned_tasks"
                                        , verbose_name="Assigned Editor")

    def __str__(self):
        return self.title

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ["edited_article", "title"],
                name="unique_edit_task_title_per_article"
            )
        ]
