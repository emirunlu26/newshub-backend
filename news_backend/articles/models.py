from ckeditor.fields import RichTextField
from django.db import models
from functools import cmp_to_key


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Name")
    slug = models.CharField(max_length=50, verbose_name="Slug")
    parent_category = models.ForeignKey(to="articles.Category", on_delete=models.CASCADE, blank=True, null=True
                                        , related_name="sub_categories", verbose_name="Parent Category")
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

    def __str__(self):
        return self.title

    @staticmethod
    def get_sorted_articles_of_region(requesting_user, region):
        def calculate_importance_score(article):
            pass
        def compare_articles(article_score_tuple1,article_score_tuple2):
            pass
        regions_to_search = [region] + region.get_all_sub_regions()
        region_slugs_to_search = [region.slug for region in regions_to_search]
        articles = (Article.objects
                    .filter(regions__slug__in=region_slugs_to_search, published_at__isnull=False)
                    .distinct())
        articles_with_scores = [(article,calculate_importance_score(article)) for article in articles]
        sorted_articles_with_scores = sorted(articles_with_scores, key=cmp_to_key(compare_articles))
        return [
            art_score_tuple[0] for art_score_tuple in sorted_articles_with_scores
        ]

    @staticmethod
    def get_sorted_articles_of_category(requesting_user, category_slug, is_parent):
        # KATEGORİ FİLTRESİ YAPARKEN IS_PARENT TRUE İSE BÜTÜN CHILD KATEGORİLERİ İLE FİLTRELEME YAPILIR
        # PRIORITY LEVEL, PUBLICATION DATE, NUMBER_OF_TAGS_FOLLOWED
        pass

class ArticleView(models.Model):
    user = models.ForeignKey(to="users.User", on_delete=models.CASCADE, verbose_name="Viewing User")
    article = models.ForeignKey(to=Article, on_delete= models.CASCADE, verbose_name="Viewed Article")
    time = models.DateTimeField(auto_now_add=True, verbose_name="View Time")
    duration_seconds = models.IntegerField(verbose_name="View Duration In Seconds")

class  ArticleBookmark(models.Model):
    user = models.ForeignKey(to="users.User", on_delete=models.CASCADE, verbose_name="Bookmarking User")
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE, verbose_name="Bookmarked Article")
    time = models.DateTimeField(auto_now_add=True, verbose_name="Bookmark Time")

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
