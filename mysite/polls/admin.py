from django.contrib import admin
from .models import Question, Choice


class ChoiceInLIne(admin.StackedInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'],
            'classes': ['collapse']}
        )
    ]

    inlines = [ChoiceInLIne]

    
admin.site.register(Question, QuestionAdmin)