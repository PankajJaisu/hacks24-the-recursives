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

from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile

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
    file_url = "https://7c5f-203-212-25-243.ngrok-free.app/static/"+file_path
    # url = "https://d192-150-107-98-252.ngrok-free.app/upload"
    
    return JsonResponse({"msg":"Done","file_path":file_url})



@api_view(['GET'])
def get_project_manager(request):

   queryset = ProjectManager.objects.all()
   data = ProjectManagerSerializer(queryset,many=True).data
   return JsonResponse({"data":data})

# @csrf_exempt
# @async_to_sync
# @api_view(['POST'])
# async def generate_ai_design(request):
#     prompt = request.POST.get('prompt')
#     if request.method == 'POST':
#         try:
#             # Get the uploaded image file
#             file = request.FILES['image']

#             # API endpoint for the first request
#             first_api_url = 'https://stablediffusionapi.com/api/v5/interior'

#             # # Prepare data for the first API request
#             # first_api_data = {
#             # "key":settings.API_KEY,
#             #     "init_image": "https://www.shutterstock.com/image-photo/russia-moscow-september-10-2019-260nw-1638165715.jpg",
#             #     "prompt": prompt,
#             #     "steps": 50,
#             #     "guidance_scale": 7
#             # }


#             ai_design = AIDesign.objects.create(image=file)
#             ai_design.image_url = settings.HOST+ai_design.image.url
#             ai_design.save()
#             last_ai_design = AIDesign.objects.filter().last()
#             # Prepare data for the first API request
#             print("url::",last_ai_design.image_url)
#             first_api_data = {
#                 "key":settings.API_KEY,
#                 "init_image":last_ai_design.image_url,
#                 "prompt": prompt,
#                 "steps": 50,
#                 "guidance_scale": 7
#             }

#             # Make the first API request
#             first_api_response = requests.post(first_api_url, json=first_api_data)

#             # Check if the request was successful (status code 200)
#             if first_api_response.status_code == 200:
#                 # Parse the response
#                 first_api_response_data = first_api_response.json()

#                 # Get the request ID from the first API response
#                 request_id = first_api_response_data.get('id')

#                 # Delay the execution for 3-4 seconds
#                 await asyncio.sleep(6)
#                 print("eee:",first_api_response_data)
#                 # API endpoint for the second request
#                 second_api_url = f'https://stablediffusionapi.com/api/v3/fetch/'

#                 # Make the second API request
#                 body ={
#                         "key":settings.API_KEY,
#                     "request_id": request_id
#                     }

#                 second_api_response = requests.post(second_api_url,json=body)

#                 # Check if the second API request was successful
#                 if second_api_response.status_code == 200:
#                     # Parse and return the second API response
#                     second_api_response_data = second_api_response.json()
#                     return JsonResponse({"data": second_api_response_data})

#                 # Return error response for the second API request
#                 return JsonResponse({'error': f'Second API request failed with status code {second_api_response.status_code}'}, status=500)

#             # Return error response for the first API request
#             return JsonResponse({'error': f'First API request failed with status code {first_api_response.status_code}'}, status=500)

#         except KeyError:
#             # Return error response for missing 'image' in the request
#             return JsonResponse({'error': 'Missing image in the request'}, status=400)
#     else:
#         # Return error for unsupported HTTP methods
#         return JsonResponse({'error': 'Method not allowed'}, status=405)
    



# @csrf_exempt
# @async_to_sync
@api_view(['POST'])
def generate_ai_design(request):
    print("request.data::",request.data)
    prompt = request.POST.get('prompt')
    if request.method == 'POST':
      
            # Get the uploaded image file
        file = request.FILES['image']

        # API endpoint for the first request
        first_api_url = 'https://stablediffusionapi.com/api/v5/interior'

        # Prepare data for the first API request
        fs = FileSystemStorage(location='media/images/')  # Adjust the path as needed
        saved_image = fs.save(file.name, ContentFile(file.read()))

        # Get the path of the saved image
        saved_image_path = fs.url(saved_image)
        print(saved_image_path)
        first_api_data = {
            "key": "xIkNooh1c70ymmqD3LLJE3k82KBSNfph0RgMd1jScHrNAweJU9w5Kj7d7ezD",
            "init_image": "https://7c5f-203-212-25-243.ngrok-free.app/media/images"+saved_image_path,
            "prompt": prompt,
            "steps": 50,
            "guidance_scale": 7
        }

        
        # Make the first API request
        first_api_response = requests.post(first_api_url, json=first_api_data)
        return JsonResponse({"data":first_api_response.json()})
            # Check if the request was successful (status code 200)
            # if first_api_response.status_code == 200:
            #     # Parse the response
            #     first_api_response_data = first_api_response.json()
            #     print(first_api_response_data)
            #     # Get the request ID from the first API response
            #     request_id = first_api_response_data.get('id')

            #     # Delay the execution for 3-4 seconds
            #     await asyncio.sleep(20)

            #     # API endpoint for the second request
            #     second_api_url = f'https://stablediffusionapi.com/api/v4/dreambooth/fetch'

            #     # Make the second API request
            #     body ={
            #             "key":"xIkNooh1c70ymmqD3LLJE3k82KBSNfph0RgMd1jScHrNAweJU9w5Kj7d7ezD",
            #             "request_id": request_id
            #         }

            #     second_api_response = requests.post(second_api_url,json=body)

            #     # Check if the second API request was successful
            #     if second_api_response.status_code == 200:
            #         # Parse and return the second API response
            #         second_api_response_data = second_api_response.json()
            #         return JsonResponse({"data": second_api_response_data})

                # Return error response for the second API request
            # return JsonResponse({'error': f'Second API request failed with status code {second_api_response.status_code}'}, status=500)

            # Return error response for the first API request
    #         return JsonResponse({'error': f'First API request failed with status code {first_api_response.status_code}'}, status=500)

    #     except KeyError:
    #         # Return error response for missing 'image' in the request
    #         return JsonResponse({'error': 'Missing image in the request'}, status=400)
    # else:
    #     # Return error for unsupported HTTP methods
    #     return JsonResponse({'error': 'Method not allowed'}, status=405)
            


@api_view(['POST'])
def upload_progress(request):
    image = request.FILES['image']
    daily_progress = DailyProgress.objects.create(image=image)
    url = "https://7c5f-203-212-25-243.ngrok-free.app"+daily_progress.image.url
    return JsonResponse({"image_url":url})





@api_view(['GET'])
def get_vendor_list(request):

   queryset = Vendor.objects.all()
   data = VendorSerializer(queryset,many=True).data
   return JsonResponse({"data":data})



@api_view(['POST'])
def add_task(request):
    data = request.data 
    Task.objects.create(task_title=data['task_title'],
                        task_description=data['task_description'],
                        deadline=data['deadline'])
    return JsonResponse({"message":"New Message Added Successfully"})


@api_view(['GET'])
def get_task(request):
    
   queryset = Task.objects.all()
   data = TaskSerializer(queryset,many=True).data
   return JsonResponse({"data":data})


