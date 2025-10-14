from django.core.management.base import BaseCommand

from core.apps.help.fixtures.initial_data import (
    HELP_ARTICLES,
    HELP_CATEGORIES,
    HELP_FAQS,
)
from core.apps.help.models.faq import FAQ
from core.apps.help.models.help_article import HelpArticle
from core.apps.help.models.help_category import HelpCategory
from core.apps.resumes.models.template import Template


class Command(BaseCommand):
    help = 'Load initial help system data'                  # noqa

    def handle(self, *args, **options):
        self.stdout.write('Loading help system data...')

        # Создаем категории
        for cat_data in HELP_CATEGORIES:
            category, created = HelpCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'title': cat_data['title'],
                    'description': cat_data['description'],
                    'order': cat_data['order'],
                },
            )
            if created:
                self.stdout.write(f'Created category: {category.title}')

        # Создаем FAQ
        for faq_data in HELP_FAQS:
            category = HelpCategory.objects.get(slug=faq_data['category'])
            faq, created = FAQ.objects.get_or_create(
                question=faq_data['question'],
                defaults={
                    'answer': faq_data['answer'],
                    'category': category,
                    'order': faq_data['order'],
                },
            )
            if created:
                self.stdout.write(f'Created FAQ: {faq.question}')

        # Создаем статьи
        for article_data in HELP_ARTICLES:
            category = HelpCategory.objects.get(slug=article_data['category'])

            # Получаем связанный шаблон если указан
            related_template = None
            if article_data.get('related_template'):
                try:
                    related_template = Template.objects.get(title=article_data['related_template'])
                except Template.DoesNotExist:
                    self.stdout.write(f"Warning: Template {article_data['related_template']} not found")

            article, created = HelpArticle.objects.get_or_create(
                slug=article_data['slug'],
                defaults={
                    'title': article_data['title'],
                    'short_description': article_data['short_description'],
                    'content': article_data['content'],
                    'category': category,
                    'tags': article_data['tags'],
                    'is_featured': article_data['is_featured'],
                    'order': article_data['order'],
                    'related_template': related_template,
                },
            )
            if created:
                self.stdout.write(f'Created article: {article.title}')

        self.stdout.write(
            self.style.SUCCESS('Successfully loaded help system data'),
        )
