from celery import shared_task
from articles.models import Article

@shared_task
def update_trending_scores():
    published_articles = Article.objects.filter(published_at__isnull=False)
    candidate_articles = [article for article in published_articles if article.was_active_recently()]

    # Kill the trending score of each non-candidate published articles
    published_articles.exclude(id__in=candidate_articles).update(trending_score=0)

    for article in candidate_articles:
        new_score = article.calculate_trending_score()
        article.trending_score = new_score

    # Bulk update for updating trending scores
    Article.objects.bulk_update(candidate_articles, ["trending_score"])