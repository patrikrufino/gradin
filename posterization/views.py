import fitz
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .forms import PosterForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PosterSerializer
import os
from django.urls import reverse
import time

def create_posters(request):
    if request.method == 'POST':
        form = PosterForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.cleaned_data['pdf_file']
            rows = int(form.cleaned_data['rows'])
            cols = int(form.cleaned_data['cols'])
            
            # Define o caminho do arquivo temporário
            temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
            file_path = os.path.join(temp_dir, pdf_file.name)

            # Verifica se o diretório 'temp' existe, se não, cria
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)

            # Salva o arquivo PDF temporário
            with open(file_path, 'wb+') as destination:
                destination.write(pdf_file.read())
                
            # Chama a função para dividir o PDF
            output_file_path = split_pdf_into_posters(file_path, "poster", rows, cols)
            
            # Prepara a resposta para download do arquivo
            with open(output_file_path, 'rb') as output_file:
                response = HttpResponse(output_file.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename={os.path.basename(output_file_path)}'
            
            # Deleta o arquivo temporário
            os.remove(file_path)
            
            return response
    else:
        form = PosterForm()
    return render(request, 'posterization/create_posters.html', {'form': form})

class CreatePostersView(APIView):
    def post(self, request):
        serializer = PosterSerializer(data=request.data)
        if serializer.is_valid():
            pdf_file = serializer.validated_data['pdf_file']
            rows = serializer.validated_data['rows']
            cols = serializer.validated_data['cols']
            
            # Define o caminho do arquivo temporário
            temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
            file_path = os.path.join(temp_dir, pdf_file.name)

            # Verifica se o diretório 'temp' existe, se não, cria
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)

            # Salva o arquivo PDF temporário
            with open(file_path, 'wb+') as destination:
                destination.write(pdf_file.read())
                
            # Chama a função para dividir o PDF
            output_file_path = split_pdf_into_posters(file_path, "poster", rows, cols)
            
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

def split_pdf_into_posters(filepath, output_prefix, rows, cols):
    pdf_doc = fitz.open(filepath)

    if len(pdf_doc) == 0:
        print("O PDF não contém páginas.")
        return None

    output_pdf = fitz.open()

    for page_number in range(len(pdf_doc)):
        page = pdf_doc[page_number]
        rect = page.rect

        piece_width = rect.width / cols
        piece_height = rect.height / rows

        for row in range(rows):
            for col in range(cols):
                x0 = col * piece_width
                y0 = row * piece_height
                x1 = x0 + piece_width
                y1 = y0 + piece_height

                piece_rect = fitz.Rect(x0, y0, x1, y1)

                new_page = output_pdf.new_page(width=piece_width, height=piece_height)
                new_page.show_pdf_page(new_page.rect, pdf_doc, page_number, clip=piece_rect)

    timestamp = int(time.time())
    output_file_path = os.path.join(settings.MEDIA_ROOT, 'temp', f"{output_prefix}_{timestamp}.pdf")
    output_pdf.save(output_file_path)
    output_pdf.close()
    pdf_doc.close()

    return output_file_path
