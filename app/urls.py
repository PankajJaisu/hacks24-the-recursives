
from django.urls import path
from . import views
urlpatterns = [
    path('hello', views.hello),
    path('generate-daily-report/',views.generate_daily_report),
    path('generate-ai-design/',views.generate_ai_design),
    path('get-project-manager/',views.get_project_manager),
    
]
