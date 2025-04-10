import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UploadFileForm
from .models import UploadedText
from .utils import calculate_tfidf

logging.basicConfig(
    filename='app.log',  
    filemode='a',        
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.DEBUG  
)

logger = logging.getLogger(__name__)

def home(request):
    logger.info("Загрузка home")
    return render(request, 'text_processor/home.html')

def upload_file(request):
    logger.info("Загрузка upload_file")
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            logger.info("Получение загруженных файлов")
            uploaded_files = request.FILES.getlist('files')
            
            try:
                text_content = []
                for f in uploaded_files:
                    content = f.read().decode('utf-8')
                    text_content.append(content)
                    logger.info(f"Файл {f.name} успешно прочитан")
            except UnicodeDecodeError as ude:
                logger.error("Ошибка декодирования файла", exc_info=True)
                messages.error(request, "Ошибка декодирования файла. Поддерживаются только текстовые файлы.")
                return redirect('text_processor:upload')
            except Exception as e:
                logger.error("Ошибка обработки файла", exc_info=True)
                messages.error(request, f"Ошибка обработки файла: {str(e)}")
                return redirect('text_processor:upload')
            
            try:
                logger.info("Вычисление TF-IDF")
                tfidf_results = calculate_tfidf(text_content)
            except Exception as e:
                logger.error("Ошибка расчета TF-IDF", exc_info=True)
                messages.error(request, f"Ошибка расчета TF-IDF: {str(e)}")
                return redirect('text_processor:upload')

            for i, uploaded_file in enumerate(uploaded_files):
                try:
                    UploadedText.objects.create(
                        file=uploaded_file,
                        tf_data=tfidf_results[i]['tf'],
                        idf_data=tfidf_results[i]['idf']
                    )
                    logger.info(f"Информация о файле {uploaded_file.name} сохранена в базе данных")
                except Exception as e:
                    logger.error(f"Ошибка сохранения файла {uploaded_file.name} в базе данных", exc_info=True)
                    messages.error(request, f"Ошибка сохранения файла {uploaded_file.name}: {str(e)}")
                    return redirect('text_processor:upload')

            sorted_results = sorted(
                tfidf_results, 
                key=lambda x: list(x['idf'].values())[0], 
                reverse=True
            )[:50]
            
            return render(request, 'text_processor/results.html', {'results': sorted_results})
        
        logger.error("Ошибка валидации формы")
        messages.error(request, "Ошибка валидации формы")
        return redirect('text_processor:upload')
    
    form = UploadFileForm()
    return render(request, 'text_processor/upload.html', {'form': form})
