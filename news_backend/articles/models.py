from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone
from datetime import timedelta
from functools import cmp_to_key
import math

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Name")
    slug = models.CharField(max_length=50, verbose_name="Slug")
    parent_category = models.ForeignKey(to="articles.Category", on_delete=models.CASCADE, blank=True, null=True
                                        , related_name="sub_categories", verbose_name="Parent Category")

    def get_all_sub_categories(self):
        sub_categories = list()

        for sub_category in self.sub_categories:
            sub_categories.append(sub_category)
            sub_categories.extend(sub_category.get_all_sub_categories())

        return sub_categories

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ["name", "parent_category"],
                name= "unique_category_name_parent_category"
            ),
            models.UniqueConstraint(
                fields = ["slug", "parent_category"],
                name = "unique_category_slug_parent_category"
            )
        ]

class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name="Name")
    slug = models.CharField(max_length=50, unique=True, verbose_name="Slug")

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Name")
    slug = models.CharField(max_length=100, unique=True, verbose_name="Slug")
    belongs_to = models.ManyToManyField(to="self", symmetrical=False, related_name="belonging_regions", blank=True
                                        , null=True, verbose_name="Belongs To")

    def get_all_sub_regions(self):
        sub_regions = list()

        for sub_region in self.belonging_regions.all():
            sub_regions.append(sub_region)
            sub_regions.extend(sub_region.get_all_sub_regions())

        return sub_regions

    def __str__(self):
        return self.name


class Article(models.Model):
    ARTICLE_TYPE_CHOICES = [
        ("news", "News Article"),
        ("opinion", "Opinion"),
        ("analysis", "Analysis")
    ]

    ARTICLE_STATUS_CHOICES = [
        ("d-in-progress", "Draft In Progress"),
        ("d-completed", "Draft Completed"),
        ("in-review", "In Review"),
        ("published", "Published")
    ]

    PRIORITY_CHOICES = [
        (3, "Breaking"),
        (2, "High Priority"),
        (1, "Important"),
        (0, "Normal"),
    ]

    DEFAULT_ARTICLE_STATUS = "d-in-progress"
    DEFAULT_PRIORITY = 0

    type = models.CharField(max_length=50, choices=ARTICLE_TYPE_CHOICES, verbose_name="Article Type")
    slug = models.CharField(max_length=100, unique=True, verbose_name="Slug")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Writing Time")
    published_at = models.DateTimeField(verbose_name="Publication Time")
    editors = models.ManyToManyField(to="users.Editor", verbose_name="Editor")
    title = models.CharField(max_length=255, verbose_name="Title")
    content = RichTextField()
    summary = models.TextField(verbose_name="Summary")
    priority_level = models.IntegerField(choices=PRIORITY_CHOICES, default= DEFAULT_PRIORITY
                                         , verbose_name="Priority Level")
    status = models.CharField(max_length=50, choices=ARTICLE_STATUS_CHOICES
                              , default=DEFAULT_ARTICLE_STATUS, verbose_name="Status")
    cover_image = models.ImageField(verbose_name="Cover Image")
    requires_premium = models.BooleanField(default=False, verbose_name="Requires Premium")
    tags = models.ManyToManyField(to=Tag, blank=True, verbose_name="Tag")
    categories = models.ManyToManyField(to=Category, verbose_name="Category")
    regions = models.ManyToManyField(to="articles.Region", verbose_name="Region")
    trending_score = models.FloatField(default=0.0, db_index=True)
    editorial_heat_score = models.FloatField(default=0.0, db_index=True)

    class Meta:
        ordering = ["-trending_score"]

    def __str__(self):
        return self.title

    def calculate_editorial_heat_score(self, current_time):
        SCALING_CONST = 25
        TIME_DECAY_GRAVITY = 1.2
        ARTICLE_AGE_OFFSET = 1

        time_delta = current_time - self.published_at
        hours_since_publication = round(time_delta.total_seconds() / 3600, 2)

        editorial_heat_score = (((self.priority_level + 1) * SCALING_CONST)
                                / pow((hours_since_publication + ARTICLE_AGE_OFFSET), TIME_DECAY_GRAVITY))

        return editorial_heat_score

    def calculate_trending_score(self, current_time):
        HOURS = 1
        TIME_DECAY_GRAVITY = 1.5
        ARTICLE_AGE_OFFSET = 2
        VIEW_WEIGHT = 1
        UNIQUE_USER_WEIGHT = 1.2
        REACTION_WEIGHT = 2
        BOOKMARK_WEIGHT = 4

        total_views_in_last_n_hour = self.calculate_total_views_in_last_n_hour(HOURS, current_time)
        number_of_unique_viewers_in_last_n_hour = self.calculate_number_of_unique_viewers_in_last_n_hour(HOURS, current_time)
        total_reactions_in_last_n_hour = self.calculate_total_reactions_in_last_n_hour(HOURS, current_time)
        total_bookmarks_in_last_n_hour = self.calculate_total_bookmarks_in_last_n_hour(HOURS, current_time)

        total_views_in_prior_n_hour = self.calculate_total_views_in_prior_n_hour(HOURS, current_time)
        number_of_unique_viewers_in_prior_n_hour = self.calculate_number_of_unique_viewers_in_prior_n_hour(HOURS, current_time)
        total_reactions_in_prior_n_hour = self.calculate_total_reactions_in_prior_n_hour(HOURS, current_time)
        total_bookmarks_in_prior_n_hour = self.calculate_total_bookmarks_in_prior_n_hour(HOURS, current_time)

        engagement_in_last_n_hour = ((total_views_in_last_n_hour * VIEW_WEIGHT)
                                     + (number_of_unique_viewers_in_last_n_hour * UNIQUE_USER_WEIGHT)
                                     + (total_reactions_in_last_n_hour * REACTION_WEIGHT)
                                     + (total_bookmarks_in_last_n_hour * BOOKMARK_WEIGHT))

        engagement_in_prior_n_hour = ((total_views_in_prior_n_hour * VIEW_WEIGHT)
                                     + (number_of_unique_viewers_in_prior_n_hour * UNIQUE_USER_WEIGHT)
                                     + (total_reactions_in_prior_n_hour * REACTION_WEIGHT)
                                     + (total_bookmarks_in_prior_n_hour * BOOKMARK_WEIGHT))

        velocity_multiplier = engagement_in_last_n_hour / (engagement_in_prior_n_hour + 1)
        velocity_multiplier = min(2, max(1, velocity_multiplier))

        time_delta = current_time - self.published_at
        hours_since_publication = round(time_delta.total_seconds() / 3600, 2)

        final_score = ((math.log10(engagement_in_last_n_hour + 1) * velocity_multiplier)
                       / pow((hours_since_publication + ARTICLE_AGE_OFFSET), TIME_DECAY_GRAVITY))

        return final_score

    def was_active_recently(self):
        HOURS = 3
        VIEW_THRESHOLD = 10
        UNIQUE_VIEWER_THRESHOLD = 5
        views = self.calculate_total_views_in_last_n_hour(HOURS)
        unique_viewers = self.calculate_number_of_unique_viewers_in_last_n_hour(HOURS)
        return views >= VIEW_THRESHOLD and unique_viewers >= UNIQUE_VIEWER_THRESHOLD

    def calculate_total_views_in_last_n_hour(self, hours, current_time):
        n_hours_ago = current_time - timedelta(hours=hours)
        total_views = ArticleView.objects.filter(article=self, created_at__gte=n_hours_ago).count()
        return total_views

    def calculate_total_views_in_prior_n_hour(self, hours, current_time):
        latest_time = current_time - timedelta(hours=hours)
        earliest_time = current_time - timedelta(hours=hours*2)
        total_views = (ArticleView.objects
                       .filter(article=self, created_at__gte=earliest_time, created_at__lt=latest_time)
                       .count())
        return total_views

    def calculate_number_of_unique_viewers_in_last_n_hour(self, hours, current_time):
        n_hours_ago = current_time - timedelta(hours=hours)

        unique_authenticated_viewers = (ArticleView.objects
         .filter(article=self, created_at__gte=n_hours_ago, user__isnull=False)
         .values("user").distinct().count())

        unique_anonymous_viewers = (ArticleView.objects
         .filter(article=self, created_at__gte=n_hours_ago, session_id__isnull=False)
         .values("session_id").distinct().count())

        return unique_authenticated_viewers + unique_anonymous_viewers

    def calculate_number_of_unique_viewers_in_prior_n_hour(self, hours, current_time):
        latest_time = current_time - timedelta(hours=hours)
        earliest_time = current_time - timedelta(hours=hours*2)

        unique_authenticated_viewers = (ArticleView.objects
                                        .filter(article=self, created_at__gte=earliest_time, created_at__lt=latest_time
                                  , user__isnull=False)
                          .values("user").distinct().count())

        unique_anonymous_viewers = (ArticleView.objects
                                        .filter(article=self, created_at__gte=earliest_time,
                                                created_at__lt=latest_time, session_id__isnull=False)
                                        .values("session_id").distinct().count())


        return unique_authenticated_viewers + unique_anonymous_viewers

    def calculate_total_reactions_in_last_n_hour(self, hours, current_time):
        n_hours_ago = current_time - timedelta(hours=hours)
        total_reactions = ArticleReaction.objects.filter(article=self, created_at__gte=n_hours_ago).count()
        return total_reactions

    def calculate_total_reactions_in_prior_n_hour(self, hours, current_time):
        latest_time = current_time - timedelta(hours=hours)
        earliest_time = current_time - timedelta(hours=hours*2)
        total_reactions = (ArticleReaction.objects
                           .filter(article=self, created_at__gte=earliest_time, created_at__lt=latest_time)
                           .count())
        return total_reactions

    def calculate_total_bookmarks_in_last_n_hour(self, hours, current_time):
        n_hours_ago = current_time - timedelta(hours=hours)
        total_bookmarks = ArticleBookmark.objects.filter(article=self, created_at__gte=n_hours_ago).count()
        return total_bookmarks

    def calculate_total_bookmarks_in_prior_n_hour(self, hours, current_time):
        latest_time = current_time - timedelta(hours=hours)
        earliest_time = current_time - timedelta(hours=hours*2)
        total_bookmarks = (ArticleBookmark.objects
                           .filter(article=self, created_at__gte=earliest_time, created_at__lt=latest_time)
                           .count())
        return total_bookmarks

class ArticleView(models.Model):
    user = models.ForeignKey(to="users.User", null=True, blank=True, on_delete=models.CASCADE
                             , related_name="article_views", verbose_name="Viewing User")
    # Use session id only for non-authenticated (anonymous) users
    session_id = models.CharField(max_length=40, null=True, blank=True, verbose_name="Session ID")
    article = models.ForeignKey(to=Article, on_delete= models.CASCADE, verbose_name="Viewed Article")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Viewed At")

class  ArticleBookmark(models.Model):
    user = models.ForeignKey(to="users.User", on_delete=models.CASCADE, verbose_name="Bookmarking User")
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE, verbose_name="Bookmarked Article")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Bookmarked At")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ["user", "article"],
                name="unique_bookmarking_user_per_article"
            )
        ]

class ArticleReaction(models.Model):
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE, related_name="reactions"
                                , verbose_name="Reacted Article")
    reaction = models.ForeignKey(to="posts.Reaction", on_delete=models.CASCADE, verbose_name="Reaction")
    reaction_owner = models.ForeignKey(to="users.User", on_delete=models.CASCADE, related_name="article_reactions"
                              , verbose_name="Reacting User")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Reacted At")

    def __str__(self):
        return (f"Article: {self.article.name}\n"
                f"Reaction: {self.reaction.name}\n"
                f"Owner: {self.reaction_owner.name}")

    @staticmethod
    def get_sorted_reactions(requesting_user, reacted_article, newest_first=True):
        CREATION_TIME_ORDER = "-created_at" if newest_first else "created_at"
        sorted_reactions_by_created_at = (((ArticleReaction.objects
                                            .filter(reaction_owner=requesting_user, article=reacted_article))
                                           .select_related("reaction"))
                                          .select_related("reaction_owner")
                                          .order_by(CREATION_TIME_ORDER))

        def compare_reactions(reaction1, reaction2):
            requesting_user_follows_reaction_1_owner = (reaction1.owner.followers
                                                        .filter(id=requesting_user.id).exists())
            requesting_user_follows_reaction_2_owner = (reaction2.owner.followers
                                                        .filter(id=requesting_user.id).exists())

            if requesting_user_follows_reaction_1_owner and not requesting_user_follows_reaction_2_owner:
                return -1
            if not requesting_user_follows_reaction_1_owner and requesting_user_follows_reaction_2_owner:
                return 1

            reaction_1_owner_is_premium = reaction1.owner.profile.is_premium()
            reaction_2_owner_is_premium = reaction2.owner.profile.is_premium()

            if reaction_1_owner_is_premium and not reaction_2_owner_is_premium:
                return -1
            if not reaction_1_owner_is_premium and reaction_2_owner_is_premium:
                return 1

            return 0

        return sorted(sorted_reactions_by_created_at, key=cmp_to_key(compare_reactions))

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
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Edit Creation Time")
    deadline = models.DateField(verbose_name="Deadline")
    completed_at = models.DateTimeField(verbose_name="Completion Time")
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
