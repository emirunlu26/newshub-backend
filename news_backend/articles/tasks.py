from celery import shared_task
from django.utils import timezone
from articles.models import Article

@shared_task
def update_trending_scores():
    current_time = timezone.now()
    published_articles = Article.objects.filter(published_at__isnull=False)
    candidate_articles = [article for article in published_articles if article.was_active_recently()]

    # Kill the trending score of each non-candidate published articles
    published_articles.exclude(id__in=candidate_articles).update(trending_score=0)

    for article in candidate_articles:
        new_score = article.calculate_trending_score(current_time=current_time)
        article.trending_score = new_score

    # Bulk update for updating trending scores
    Article.objects.bulk_update(candidate_articles, ["trending_score"])

@shared_task
def update_editorial_heat_scores():
    DAY_LIMIT = 3

    current_time = timezone.now()
    lower_time_limit = current_time - timezone.timedelta(days=DAY_LIMIT)
    candidate_articles = Article.objects.filter(published_at__gte=lower_time_limit)

    # Kill the editorial hit score of each non-candidate published articles
    Article.objects.filter(published_at__isnull=False).exclude(id__in=candidate_articles).update(editorial_heat_score=0)

    for article in candidate_articles:
        new_score = article.calculate_editorial_heat_score(current_time=current_time)
        article.editorial_heat_score = new_score

    # Bulk update for updating editorial heat scores
    Article.objects.bulk_update(candidate_articles, ['editorial_heat_score'])