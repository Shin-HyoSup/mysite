from django.contrib import admin
from .models import Question
from .models import Choice

# Register your models here.
# admin.site.register(Question)
# admin.site.register(Choice)

class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text','pub_date','was_publish_recently')
    fieldsets = [
        (None,          {'fields':['question_text']}),
        ("Data Info",   {'fields':['pub_date']}),
    ]
    inlines = [ChoiceInLine]

admin.site.register(Question, QuestionAdmin)

