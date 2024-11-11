from django.contrib import admin
from .models import Question, Answer, QuestionLike, AnswerLike

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'author', 'created_at')

class QuestionLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'question', 'created_at')

class AnswerLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'answer', 'created_at')

# Регистрация моделей
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(QuestionLike, QuestionLikeAdmin)
admin.site.register(AnswerLike, AnswerLikeAdmin)
