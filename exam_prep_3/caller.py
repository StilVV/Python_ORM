import os
import django
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Count, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import *


# Create queries within functions
def get_authors(search_name=None, search_email=None) -> str:
    if search_name is None and search_email is None:
        return ""

    query_name = Q(full_name__icontains=search_name) if search_name else None
    query_email = Q(email__icontains=search_email) if search_email else None

    if query_name and query_email:
        query = query_name & query_email
    elif query_name:
        query = query_name
    else:
        query = query_email

    authors = Author.objects.filter(query).order_by('-full_name')

    if not authors.exists():
        return ""

    def banned_status(author):
        return "Banned" if author.is_banned else "Not Banned"

    result = '\n'.join(
        f'Author: {author.full_name}, email: {author.email}, status: {banned_status(author)}'
        for author in authors
    )

    return result


def get_top_publisher() -> str:
    author = Author.objects.get_authors_by_article_count().first()

    if not author:
        return ""

    return f"Top Author: {author.full_name} with {author.article_count} published articles."


def get_top_reviewer() -> str:
    authors = Author.objects.annotate(
        review_count=Count('reviews')
    ).order_by('-review_count', 'email').first()

    return f"Top Reviewer: {authors.full_name} with {authors.review_count} published reviews."


def get_latest_article():
    latest_article = Article.objects.prefetch_related('authors', 'reviews').order_by('-published_on').first()

    if latest_article is None:
        return ""

    authors_names = ', '.join(author.full_name for author in latest_article.authors.all().order_by('full_name'))
    num_reviews = latest_article.reviews.count()
    avg_rating = sum([r.rating for r in latest_article.reviews.all()]) / num_reviews if num_reviews else 0.0

    return f"The latest article is: {latest_article.title}. Authors: {authors_names}. Reviewed: {num_reviews} times." \
           f" Average Rating: {avg_rating:.2f}."


def get_top_rated_article() -> str:
    top_rated_article = Article.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    ).order_by('-avg_rating', 'title').first()

    if top_rated_article is None:
        return ""

    avg_rating = top_rated_article.avg_rating if top_rated_article.avg_rating is not None else 0.0
    num_reviews = top_rated_article.review_count

    return (f"The top-rated article is: {top_rated_article.title}, with an average rating of {avg_rating:.2f}, "
            f"reviewed {num_reviews} times.")


def ban_author(email=None) -> str:
    if email is None:
        return "No authors banned."

    try:
        author = Author.objects.prefetch_related('reviews').get(email=email)
    except ObjectDoesNotExist:
        return "No authors banned."

    num_of_reviews = author.reviews.count()

    author.is_banned = True
    author.save()

    author.reviews.all().delete()

    return f"Author: {author.full_name} is banned! {num_of_reviews} reviews deleted."
