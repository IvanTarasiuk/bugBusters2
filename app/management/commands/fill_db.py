from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike
import random

class Command(BaseCommand):
    help = 'Fill database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Ratio of test data')

    def create_user_ovr(self, username, password="password"):
        # Проверяем, существует ли уже пользователь с таким именем
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            return user
        else:
            print(f"Пользователь {username} уже существует")
            return User.objects.get(username=username)

    def create_tag_ovr(self, tag_name):
        # Проверяем, существует ли уже тег с таким именем
        tag, created = Tag.objects.get_or_create(name=tag_name)
        if created:
            print(f"Создан новый тег: {tag_name}")
        else:
            print(f"Тег {tag_name} уже существует")
        return tag

    def handle(self, *args, **options):
        ratio = options['ratio']

        # Создаем пользователей
        users = []
        for i in range(ratio):
            username = f'user{i}'
            user = self.create_user_ovr(username=username, password='password')
            users.append(user)

        def create_answer_likes(self, num_likes=10):
            answers = list(Answer.objects.all())
            users = list(User.objects.all())

            for _ in range(num_likes):
                user = random.choice(users)
                answer = random.choice(answers)

                # Проверка на существование такой комбинации user-answer (для уникальности)
                if not AnswerLike.objects.filter(user=user, answer=answer).exists():
                    AnswerLike.objects.create(user=user, answer=answer)
                    print(f'AnswerLike создан для пользователя {user} и ответа {answer}')
                else:
                    print(f'AnswerLike для пользователя {user} и ответа {answer} уже существует')

        # Вызов функции для заполнения AnswerLike
        create_answer_likes(self, 20)

        # Создаем теги с проверкой на уникальность
        tags = []
        for i in range(ratio):
            tag_name = f'tag{i}'
            tag = self.create_tag_ovr(tag_name)
            tags.append(tag)

        # Создаем вопросы и ответы
        questions = []
        for i in range(ratio * 10):
            question = Question.objects.create(
                author=random.choice(users),
                title=f'Question title {i}',
                text=f'Question text {i}'
            )
            question.tags.set(random.sample(tags, k=random.randint(1, 3)))
            questions.append(question)

        answers = []
        for question in questions:
            for _ in range(random.randint(1, ratio * 10)):
                answer = Answer.objects.create(
                    question=question,
                    author=random.choice(users),
                    text=f'Answer text for {question.title}'
                )
                answers.append(answer)

        # Создаем лайки для вопросов с проверкой на уникальность
        for _ in range(ratio * 200):
            user = random.choice(users)
            question = random.choice(questions)
            # Проверяем, не поставил ли этот пользователь уже лайк на данный вопрос
            if not QuestionLike.objects.filter(user=user, question=question).exists():
                QuestionLike.objects.create(user=user, question=question)

        # Создаем лайки для ответов с проверкой на уникальность
        for _ in range(ratio * 200):
            user = random.choice(users)
            answer = random.choice(answers)
            # Проверяем, не поставил ли этот пользователь уже лайк на данный ответ
            if not AnswerLike.objects.filter(user=user, answer=answer).exists():
                AnswerLike.objects.create(user=user, answer=answer)

        self.stdout.write(self.style.SUCCESS('Database successfully filled with test data'))
