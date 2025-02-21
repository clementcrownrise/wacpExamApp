from django.contrib import admin
from .models import Letter

# Register your models here.
@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
        list_display = ["examination","surname","name","institutionAddress","email"]

        #def examName(self,obj):
        #    return obj.letter.examName
    

#admin.site.register(Letter, LetterAdmin)


