import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from FlashCardApp.models import Deck, Question, Card, Subject

User = get_user_model()


class Command(BaseCommand):
    help = 'Generates random flash cards'

    def add_arguments(self, parser):
        parser.add_argument('num_decks', type=int,
                            help='The number of decks to create')
        parser.add_argument('num_cards_per_deck', type=int,
                            help='The number of cards per deck')

    def handle(self, *args, **options):
        num_decks = options['num_decks']
        num_cards_per_deck = options['num_cards_per_deck']
        fake = Faker()

        # Get or create a user
        user, created = User.objects.get_or_create(username='testuser')
        if created:
            user.set_password('testpassword')
            user.save()
            self.stdout.write(self.style.SUCCESS(
                'Created test user: testuser'))

        subjects = self.get_or_create_subjects(fake)

        for _ in range(num_decks):
            deck = self.create_deck(fake, user, subjects)
            self.stdout.write(self.style.SUCCESS(f'Created deck: {deck.name}'))

            for _ in range(num_cards_per_deck):
                question = self.create_question(fake, subjects)
                card = self.create_card(deck, question)
                self.stdout.write(self.style.SUCCESS(
                    f'Created card for question: {question.question[:30]}...'))

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {num_decks} decks with {num_cards_per_deck} cards each'))

    def get_or_create_subjects(self, fake, target_count=5):
        existing_subjects = list(Subject.objects.all())
        subjects_to_create = max(0, target_count - len(existing_subjects))

        for _ in range(subjects_to_create):
            subject, created = Subject.objects.get_or_create(
                name=fake.unique.word(),
                defaults={'description': fake.sentence()}
            )
            if created:
                existing_subjects.append(subject)
                self.stdout.write(self.style.SUCCESS(
                    f'Created new subject: {subject.name}'))

        return existing_subjects

    def create_deck(self, fake, user, subjects):
        return Deck.objects.create(
            name=fake.unique.catch_phrase(),
            subject=random.choice(subjects),
            author=user,
            description=fake.text()
        )

    def create_question(self, fake, subjects):
        question_type = random.choice(Question.QuestionType.choices)[0]
        difficulty = random.choice(Question.QuestionDifficulty.choices)[0]
        subject = random.choice(subjects)

        base_fields = {
            'type': question_type,
            'difficulty': difficulty,
            'subject': subject,
            'question': fake.sentence(),
        }

        if question_type == Question.QuestionType.MULTIPLE_CHOICE:
            base_fields.update({
                'answer': fake.word(),
                'answer_2': fake.word(),
                'answer_3': fake.word(),
                'answer_4': fake.word(),
            })
        elif question_type == Question.QuestionType.TRUE_FALSE:
            base_fields['answer'] = random.choice(['True', 'False'])
        elif question_type == Question.QuestionType.FREE_TEXT:
            base_fields['answer'] = fake.word()
        else:  # NUMERIC
            base_fields['answer'] = str(fake.random_number())

        return Question.objects.create(**base_fields)

    def create_card(self, deck, question):
        return Card.objects.create(deck=deck, question=question)
