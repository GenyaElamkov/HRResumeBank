from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import (
    DetailView,
    ListView,
)

from .models.faq import FAQ
from .models.help_article import HelpArticle
from .models.help_category import HelpCategory


class HelpHomeView(ListView):
    """Главная страница справочной системы"""
    template_name = 'help/help_home.html'
    context_object_name = 'featured_articles'

    def get_queryset(self):
        return HelpArticle.objects.filter(
            is_published=True,
            is_featured=True,
        )[:8]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = HelpCategory.objects.filter(
            is_active=True,
            parent__isnull=True,
        ).prefetch_related('children')
        context['faqs'] = FAQ.objects.filter(is_published=True)[:10]
        return context


class HelpCategoryView(DetailView):
    """Просмотр категории с статьями"""
    model = HelpCategory
    template_name = 'help/help_category.html'
    context_object_name = 'category'

    def get_queryset(self):
        return HelpCategory.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = HelpArticle.objects.filter(
            category=self.object,
            is_published=True,
        )
        context['child_categories'] = HelpCategory.objects.filter(
            parent=self.object,
            is_active=True,
        )
        return context


class HelpArticleView(DetailView):
    """Просмотр статьи справки"""
    model = HelpArticle
    template_name = 'help/help_article.html'
    context_object_name = 'article'

    def get_queryset(self):
        return HelpArticle.objects.filter(is_published=True)

    def get_object(self):
        obj = super().get_object()
        # Увеличиваем счетчик просмотров
        obj.view_count += 1
        obj.save(update_fields=['view_count'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Похожие статьи
        context['related_articles'] = HelpArticle.objects.filter(
            category=self.object.category,
            is_published=True,
        ).exclude(id=self.object.id)[:5]
        return context


class HelpSearchView(ListView):
    """Поиск по справочной системе"""
    template_name = 'help/help_search.html'
    context_object_name = 'results'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '').strip()
        if not query:
            return redirect(reverse('help_system:help_home'))
        return super().get(request=request, *args, **kwargs)

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return HelpArticle.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(short_description__icontains=query) |
                Q(tags__icontains=query),
                is_published=True,
            )
        return HelpArticle.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class FAQListView(ListView):
    """Страница часто задаваемых вопросов"""
    model = FAQ
    template_name = 'help/faq_list.html'
    context_object_name = 'faqs'

    def get_queryset(self):
        return FAQ.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Группировка FAQ по категориям
        categories = HelpCategory.objects.filter(
            is_active=True,
            faqs__isnull=False,
        ).distinct()
        context['categories'] = categories
        return context
