from django.db import models

# Create your models here.

class Reaction(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Name")
    icon = models.ImageField(upload_to="reaction_icons/", verbose_name="Icon")

    def __str__(self):
        return self.name

class Post(models.Model):
    owner = models.ForeignKey(to="users.User", on_delete=models.CASCADE, related_name="posts", verbose_name="Owner")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation Time")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Update Time",)
    referenced_article = models.ForeignKey(to="articles.Article", on_delete=models.SET_NULL
                                           , blank=True, null=True, verbose_name="Referenced Article")
    referenced_post = models.ForeignKey(to="self", blank=True, null=True, on_delete=models.SET
                                        , verbose_name="Referenced Post")
    content = models.TextField(verbose_name="Content")

    def __str__(self):
        return self.content

class PostImage(models.Model):
    DEFAULT_RANK = -1 # no ranked assigned value
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="images", verbose_name="Post")
    image = models.ImageField(upload_to="post_images/", verbose_name="Image")
    rank = models.IntegerField(default=DEFAULT_RANK, verbose_name="Rank of Image in Post")

class Comment(models.Model):
    owner = models.ForeignKey(to="users.User", on_delete=models.CASCADE, related_name="comments", verbose_name="Owner")
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="comments", verbose_name="Post")
    content = models.TextField(verbose_name="Content")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation Time")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Update Time")
    parent_comment = models.ForeignKey(to="self", on_delete=models.CASCADE, related_name="child_comments"
                                       , blank=True, null=True, verbose_name="Parent Comment")

    @staticmethod
    def is_content_valid(content):
        MAX_LENGTH = 1000
        CONTENT_NOT_STRING_ERROR = "Content must be type of string."
        CONTENT_LENGTH_ERROR = f"The length of the content should be between 1 - {MAX_LENGTH}"
        CONTENT_VALID = ""
        if not isinstance(content, str):
            return False, CONTENT_NOT_STRING_ERROR
        content_len = len(content)
        content_len_valid = content_len > 0 and content_len <= MAX_LENGTH
        if content_len_valid:
            return True, CONTENT_VALID
        else:
            return False, CONTENT_LENGTH_ERROR

class PostReaction(models.Model):
        post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="reactions"
                                 , verbose_name="Reacted Post")
        reaction = models.ForeignKey(to=Reaction, on_delete=models.CASCADE, verbose_name="Reaction")
        reaction_owner = models.ForeignKey(to="users.User", on_delete=models.CASCADE, related_name="post_reactions"
                                           , verbose_name="Reaction Owner")
        created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation Time")

        class Meta:
            constraints = [
                models.UniqueConstraint(
                    fields=["post", "reaction_owner"],
                    name="unique_user_reaction_per_post"
                )
            ]


class CommentReaction(models.Model):
    comment = models.ForeignKey(to=Comment, on_delete=models.CASCADE, related_name="reactions"
                             , verbose_name="Reacted Comment")
    reaction = models.ForeignKey(to=Reaction, on_delete=models.CASCADE, verbose_name="Reaction")
    reaction_owner = models.ForeignKey(to="users.User", on_delete=models.CASCADE, related_name="comment_reactions"
                                       , verbose_name="Reaction Owner")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation Time")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ["comment", "reaction_owner"],
                name="unique_user_reaction_per_comment"
            )
        ]