# views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PosterSerializer
import os
from django.urls import reverse
from .utils.tiling import Tiling
from typing import Any

class TilingView(APIView):
    def post(self, request: Any) -> Response:  # Adicionando anotações de tipo
        serializer = PosterSerializer(data=request.data)
        if serializer.is_valid():
            pdf_file = serializer.validated_data['pdf_file']
            rows = serializer.validated_data['rows']
            cols = serializer.validated_data['cols']
            
            # Define o caminho do arquivo temporário
            temp_dir: str = os.path.join(settings.MEDIA_ROOT, 'temp')
            file_path: str = os.path.join(temp_dir, pdf_file.name)

            # Verifica se o diretório 'temp' existe, se não, cria
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)

            # Salva o arquivo PDF temporário
            with open(file_path, 'wb+') as destination:
                destination.write(pdf_file.read())
                
            # Chama a função para dividir o PDF
            tiling = Tiling(file_path)
            output_file_path = tiling.pdf_file("poster", rows, cols)
            
            # Gera a URL para o arquivo gerado
            output_file_name = os.path.basename(output_file_path)
            output_file_url = request.build_absolute_uri(f"{settings.MEDIA_URL}temp/{output_file_name}")
            
            # Deleta o arquivo temporário
            os.remove(file_path)
            
            # Verifica se o arquivo gerado realmente existe
            if not os.path.exists(output_file_path):
                return Response({'error': 'Arquivo gerado não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
            
            return Response({'download_url': output_file_url}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
