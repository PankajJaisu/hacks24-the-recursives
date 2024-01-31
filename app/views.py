from django.shortcuts import render

from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.template.loader import get_template
import pdfkit
from .models import AIDesign
from pathlib import Path
import requests
import random 
import asyncio
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .serializers import *
from django.conf import settings

from asgiref.sync import async_to_sync

@api_view(['GET'])
def hello(request):
    return JsonResponse({"message":"Hello"})

def render_to_pdf(template_src, context, file_name="invoice"):
    Path("static/prescription/").mkdir(parents=True, exist_ok=True)
    file_path = f'prescription/{file_name}_{str(random.randint(100000, 9999999))}.pdf'
    print("file_path::",file_path)
    template = get_template(template_src)
    print("template::",template)
    html = template.render(context)
    options = {
       'page-height': '270mm',
        'page-width': '185mm',
    }
    pdf = pdfkit.from_string(html, r'static/' + file_path, options=options)
    return pdf,file_path

@api_view(['POST'])
def generate_daily_report(request):
    template_src = 'daily_report.html'
    data = {}
    random_integer = random.randint(1, 100)
    temp, file_path = render_to_pdf(template_src, data, f'report_{random_integer}')
    # file_url = "https://24c3-150-107-98-252.ngrok-free.app/static/"+file_path
    # url = "https://d192-150-107-98-252.ngrok-free.app/upload"
    
    return JsonResponse({"msg":"Done","file_path":"done"})



@api_view(['GET'])
def get_project_manager(request):

   queryset = ProjectManager.objects.all()
   data = ProjectManagerSerializer(queryset,many=True).data
   return JsonResponse({"data":data})

@csrf_exempt
@async_to_sync
@api_view(['POST'])
async def generate_ai_design(request):
    prompt = request.POST.get('prompt')
    
    try:
        # Get the uploaded image file
        file = request.FILES['image']

        # API endpoint for the first request
        first_api_url = 'https://stablediffusionapi.com/api/v5/interior'
        ai_design = AIDesign.objects.create(image=file)
        ai_design.image_url = settings.HOST+ai_design.image.url
        ai_design.save()
        last_ai_design = AIDesign.objects.filter().last()
        # Prepare data for the first API request
        print("url::",last_ai_design.image_url)
        first_api_data = {
            "key":settings.API_KEY,
            "init_image":last_ai_design.image_url,
            "prompt": prompt,
            "steps": 50,
            "guidance_scale": 7
        }

       
        first_api_response = requests.post(first_api_url, json=first_api_data)

        # Check if the request was successful (status code 200)
        if first_api_response.status_code == 200:
            # Parse the response
            first_api_response_data = first_api_response.json()

            # Get the request ID from the first API response
            request_id = first_api_response_data.get('id')

            # Delay the execution for 3-4 seconds
            await asyncio.sleep(6)
            print("eee:",first_api_response_data)
            # API endpoint for the second request
            second_api_url = f'https://stablediffusionapi.com/api/v3/fetch/{request_id}'

            # Make the second API request
            body ={
                    "key":settings.API_KEY,
                "request_id": "71149552"
                }

            second_api_response = requests.post(second_api_url,json=body)

            # Check if the second API request was successful
            if second_api_response.status_code == 200:
                # Parse and return the second API response
                second_api_response_data = second_api_response.json()
                return JsonResponse({"data": second_api_response_data})

            # Return error response for the second API request
            return JsonResponse({'error': f'Second API request failed with status code {second_api_response.status_code}'}, status=500)

        # Return error response for the first API request
        return JsonResponse({'error': f'First API request failed with status code {first_api_response.status_code}'}, status=500)

    except KeyError:
        # Return error response for missing 'image' in the request
        return JsonResponse({'error': 'Missing image in the request'}, status=400)


