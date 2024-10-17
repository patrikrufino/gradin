import fitz
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .forms import PosterForm
import os

def create_posters(request):
    if request.method == 'POST':
        form = PosterForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.cleaned_data['pdf_file']
            rows = int(form.cleaned_data['rows'])  # Converte para inteiro
            cols = int(form.cleaned_data['cols'])  # Converte para inteiro
            
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

def split_pdf_into_posters(filepath, output_prefix, rows, cols):
    """
    Divide uma única página de um PDF em múltiplas partes, organizando as partes em uma grade.

    Args:
        filepath: Caminho para o arquivo PDF de entrada.
        output_prefix: Prefixo para os nomes dos arquivos de saída.
        rows: Número de linhas na grade de pôsteres.
        cols: Número de colunas na grade de pôsteres.
    """
    pdf_doc = fitz.open(filepath)

    # Verifica se há pelo menos uma página
    if len(pdf_doc) == 0:
        print("O PDF não contém páginas.")
        return None

    # Obtém a primeira página
    page = pdf_doc[0]
    rect = page.rect

    # Calcula a largura e altura de cada parte
    piece_width = rect.width / cols
    piece_height = rect.height / rows

    output_pdf = fitz.open()

    # Divide a página em partes
    for row in range(rows):
        for col in range(cols):
            # Calcula a posição do retângulo para a parte
            x0 = col * piece_width
            y0 = row * piece_height
            x1 = x0 + piece_width
            y1 = y0 + piece_height

            # Cria um novo retângulo para a parte
            piece_rect = fitz.Rect(x0, y0, x1, y1)

            # Adiciona uma nova página ao PDF de saída
            new_page = output_pdf.new_page(width=piece_width, height=piece_height)

            # Copia a parte da página original para a nova página
            new_page.show_pdf_page(new_page.rect, pdf_doc, 0, clip=piece_rect)

    # Define o caminho do arquivo de saída
    output_file_path = os.path.join(settings.MEDIA_ROOT, 'temp', f"{output_prefix}.pdf")
    
    # Salva o PDF de saída
    output_pdf.save(output_file_path)
    output_pdf.close()
    pdf_doc.close()

    return output_file_path
