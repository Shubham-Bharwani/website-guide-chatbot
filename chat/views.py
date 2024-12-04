from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, URLEntryForm
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import QueryHistory, ScrapeHistory
from .scraping_logic import ScrapeData
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
import google.generativeai as genai
from chat import serializers
from rest_framework import status
import os
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIRequestFactory
from django.conf import settings
from django.utils import timezone
import json
from django.http import JsonResponse
from markdown import markdown
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control, never_cache
from django.core.cache import cache
from dotenv import load_dotenv
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, "chat/register.html", {'form': form})

@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_view(request):
    cache.clear()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                try:
                    user_history = QueryHistory.objects.get(user=user)
                    if user_history is not None :
                        return redirect('chat')
                except:
                    pass
                return redirect('url_entry')
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'chat/login.html', {'form': form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def url_entry_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    print("Entered View")
    
    if request.method == 'POST':
        form = URLEntryForm(request.POST)
        print("Form is valid")
        if form.is_valid():
            print(form.cleaned_data)
            site_name = form.cleaned_data['site_name']
            site_url = form.cleaned_data['site_url']
            try:
                print("Enters Scraping")
                scrape_history = ScrapeHistory.objects.get(site_name=site_name)
                if timezone.now() - scrape_history.last_updated > timedelta(hours=24):
                    print("Time difference --> ", timezone.now() - scrape_history.last_updated)
                    return render(request,'chat/url_entry.html',{'dataExist':'true','form':form})
                else:   
                    print("Scraping passed")
                    pass
            except ScrapeHistory.DoesNotExist:
                # Modal showing a loader for "Scrapping in Progress. . . Please do not Close this window."
                ScrapeData(site_url, site_name)
                ScrapeHistory.objects.create(site_name= site_name,last_updated = datetime.now())
            finally:
            # # If user selects 'No' the function moves here.
                return redirect('chat')
    check_history = QueryHistory.objects.filter(user = request.user)
    if check_history:
        return redirect('chat')
    else:
        form = URLEntryForm()
    return render(request, 'chat/url_entry.html', {'form': form})

load_dotenv()
gemini_api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-1.5-flash')
# chat = model.start_chat()

# @method_decorator(never_cache)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home_view(request):
    return redirect('login')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required 
def logout_view(request):
    logout(request)
    request.session.flush()
    cache.clear()
    return redirect('home')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    sites = ScrapeHistory.objects.values_list('site_name')
    
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        query = data.get('message')
        sitename = data.get('site_name')
        
        if not query or not sitename:
            return JsonResponse({'error': 'Query and Site Name are required!'}, status=400)
        
        print("Details:", query, sitename)
        
        # Simulating API call and response
        user_history = QueryHistory.objects.filter(user=request.user).values('query','response')
        factory = APIRequestFactory()
        query_params = {'query': query, "scrape_context": sitename}
        api_request = factory.post('/api/answer/', data=query_params)
        api = AskGemini.as_view()
        answer_response = api(api_request)
        answer = answer_response.data.get('response', "Sorry, I couldn't process that.")
        
        # Save the query and answer in the user's history
        QueryHistory.objects.create(user=request.user, query=query, response=answer)
        return JsonResponse({'response': answer})
    
    user_history = QueryHistory.objects.filter(user=request.user).values('query','response')
    context = {
        'history': user_history,
        'sites': sites
    }
    return render(request, 'chat/chatbot.html', context)


class AskGemini(APIView):
    serializer_class = serializers.AskSerializer
    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        print("Request:" ,request.data)
        if serializer.is_valid():

            query = serializer.validated_data.get('query')
            name = serializer.validated_data.get('scrape_context')

            file_path = os.path.join(settings.MEDIA_ROOT,f"{name}.txt")
            if os.path.exists(file_path):
                with open(file_path,'r',encoding='utf-8') as data:
                    print("TEXT is")
                    text = data.read()
                    # print("TEXT is",text) 
            else:
                return Response({
                    'response': 'Data not found'
                })
            chat_response_mark = model.generate_content(f"You name is Scrat. As being a Chatbot Guide for company {name} be professional and answer intelligently and a little descriptively the query about the company using the given context\n\nQuery: {query}\n\nContext: {text}")
            # chat_response = chat_response_mark.text.replace("*",'')
            chat_response = markdown(chat_response_mark.text)
            print(chat_response)
            return Response({
                'query':query,
                'response': chat_response,
            })
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



