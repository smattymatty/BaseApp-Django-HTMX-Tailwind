from django.db import models
from django.conf import settings


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Deck(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        null=True,
        default=None
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    class QuestionType(models.TextChoices):
        MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
        FREE_TEXT = "FREE_TEXT"
        TRUE_FALSE = "TRUE_FALSE"
        NUMERIC = "NUMERIC"

    class QuestionDifficulty(models.TextChoices):
        EASY = "EASY"
        MEDIUM = "MEDIUM"
        HARD = "HARD"
    type = models.CharField(
        max_length=100,
        choices=QuestionType.choices
    )
    difficulty = models.CharField(
        max_length=100,
        choices=QuestionDifficulty.choices,
        default=QuestionDifficulty.EASY
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.SET_NULL,
        null=True,
        default=None
    )
    question = models.TextField()
    # the first answer is the correct one
    # the rest are wrong answers for multiple choice questions
    answer = models.TextField()
    answer_2 = models.TextField(null=True, blank=True)
    answer_3 = models.TextField(null=True, blank=True)
    answer_4 = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question


class Card(models.Model):
    deck = models.ForeignKey(
        Deck, on_delete=models.CASCADE,
        related_name="cards"
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    correct_attempts = models.IntegerField(default=0)
    total_attempts = models.IntegerField(default=0)
    last_attempt_date = models.DateTimeField(auto_now=True)
