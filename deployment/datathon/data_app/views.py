import os
import subprocess
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def upload_and_process_image(request):
    if 'photo' not in request.FILES:
        return Response({"error": "No photo in request"}, status=status.HTTP_400_BAD_REQUEST)

    uploaded_file = request.FILES['photo']
    file_name = default_storage.get_available_name('photo.jpg')

    # Save the image
    try:
        path = default_storage.save(file_name, ContentFile(uploaded_file.read()))
        full_image_path = os.path.join(settings.MEDIA_ROOT, path)
    except Exception as e:
        return Response({"error": f"Error saving image: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    script_path = os.path.join(settings.BASE_DIR, 'data_app', 'checkcam.py')

    # Debug output
    print(f"Script Path: {script_path}")
    print(f"Full Image Path: {full_image_path}")

    try:
        result = subprocess.run([sys.executable, script_path, full_image_path], 
                                capture_output=True, text=True, check=True)
        
        print(f"Script Output: {result.stdout}")
        print(f"Script Error: {result.stderr}")
        
    except subprocess.CalledProcessError as e:
        print(f"Script execution failed: {e.stderr}")
        return Response({"error": f"Error executing script: {e.stderr}"}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        print(f"Exception during script execution: {str(e)}")
        return Response({"error": f"Exception during script execution: {str(e)}"}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"result": result.stdout}, status=status.HTTP_200_OK)