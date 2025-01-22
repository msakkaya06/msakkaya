
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import import_computer_data_from_excel  # Veritabanına import işlemi
import os

# Create your views here.
@api_view(['POST'])
def upload_excel(request):
    try:
        # Dosya yolunu parametre olarak alıyoruz
        file_path = request.data.get('filePath')
        
        if file_path is None:
            return Response({"message": "File path not provided"}, status=400)

        # Excel dosyasını açma ve kaydetme işlemi
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
   
        # Excel dosyasını import et
        import_computer_data_from_excel(file_path)
        
        return Response({"message": "Excel file imported successfully!"}, status=200)

    except Exception as e:
        return Response({"message": str(e)}, status=400)
