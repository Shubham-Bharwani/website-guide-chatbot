from django.urls import path
from . import views
urlpatterns = [
    path("", views.home_view, name="home"),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('register/',views.register_view,name='register'),
    path('url-entry/',views.url_entry_view,name='url_entry'),
    path('chat/',views.chat_view,name='chat'),
    path('api/answer',views.AskGemini.as_view(),name='answer')
]
