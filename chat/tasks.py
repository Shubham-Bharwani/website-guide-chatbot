from chatbot.celery import app
from .scraping_logic import ScrapeData
from .models import ScrapeHistory
from datetime import timedelta, datetime
from django.utils import timezone
@app.task
def scrape_after_every_6_hours():
    scrape_history = ScrapeHistory.objects.filter()
    for i in scrape_history:
        print(i.last_updated)
        if timezone.now() - i.last_updated > timedelta(hours=6):
            print(i.last_updated)
            ScrapeData(i.site_url,i.site_name)
            i.last_updated = datetime.now()
            i.save()
            print(i.last_updated)
            print(i.site_name," Scraped at ", datetime.now())
    return "success"