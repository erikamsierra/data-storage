from django.contrib import admin

from data_storage import models


@admin.register(models.Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'birth_date')
    search_fields = ('full_name',)


@admin.register(models.Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)


@admin.register(models.Championship)
class ChampionshipAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year')
    search_fields = ('name',)
