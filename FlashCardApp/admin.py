from django.contrib import admin
from django.db.models import Count
from .models import Deck, Question, Card, UserProgress, Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'deck_count', 'question_count')
    search_fields = ('name',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            deck_count=Count('deck', distinct=True),
            question_count=Count('question', distinct=True)
        )
        show_facets = admin.ShowFacets.ALWAYS
        return queryset

    def deck_count(self, obj):
        return obj.deck_count
    deck_count.admin_order_field = 'deck_count'

    def question_count(self, obj):
        return obj.question_count
    question_count.admin_order_field = 'question_count'


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'author', 'card_count', 'created_at')
    list_filter = ('subject', 'author', 'created_at')
    search_fields = ('name', 'subject__name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ['subject', 'author']
    show_facets = admin.ShowFacets.ALWAYS
    fieldsets = (
        (None, {
            'fields': ('name', 'subject', 'author', 'description')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),

    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(card_count=Count('card'))
        return queryset

    def card_count(self, obj):
        return obj.card_count
    card_count.admin_order_field = 'card_count'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'subject', 'type', 'difficulty', 'created_at')
    list_filter = ('subject', 'type', 'difficulty', 'created_at')
    search_fields = ('question', 'answer', 'subject__name')
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ['subject']
    show_facets = admin.ShowFacets.ALWAYS
    fieldsets = (
        (None, {
            'fields': ('question', 'subject', 'type', 'difficulty')
        }),
        ('Answers', {
            'fields': ('answer', 'answer_2', 'answer_3', 'answer_4')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'deck', 'question', 'created_at')
    list_filter = ('deck__subject', 'deck', 'created_at')
    search_fields = ('deck__name', 'question__question')
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ['deck', 'question']
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'card', 'correct_attempts',
                    'total_attempts', 'last_attempt_date')
    list_filter = ('user', 'card__deck__subject',
                   'card__deck', 'last_attempt_date')
    search_fields = ('user__username', 'card__deck__name')
    readonly_fields = ('last_attempt_date',)
    autocomplete_fields = ['user', 'card']
    show_facets = admin.ShowFacets.ALWAYS

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related(
            'user', 'card__deck', 'card__deck__subject')
        return queryset
