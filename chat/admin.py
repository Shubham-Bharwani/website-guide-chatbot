from django.contrib import admin
from django.utils import timezone
from chat.models import ScrapeHistory,QueryHistory
# Register your models here.
class ScrapeAdmin(admin.ModelAdmin):
    list_display = ['name','last_update']
    @admin.display(description='Site Name')
    def name(self,obj):
        return obj.site_name
    @admin.display(description='Last Updated')
    def last_update(self,obj):
        td = (timezone.now()-obj.last_updated)
        days = td.days
        hours, remainder = divmod(td.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds ago"

class QueryAdmin(admin.ModelAdmin):
    list_display = ('user','query')

admin.site.register(ScrapeHistory, ScrapeAdmin)
admin.site.register(QueryHistory, QueryAdmin)