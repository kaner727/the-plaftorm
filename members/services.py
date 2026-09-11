from django.core.files.storage import default_storage
import os 

def build_lesson_content(lesson_type, post_data, files=None):
    builders = {
        'video':   lambda: {'url': post_data.get('video_url', '')},
        'text':    lambda: {'content': post_data.get('text_content', '')},
        'choices': lambda: _build_questions(post_data),
        'pdf':     lambda: _build_pdf(files, post_data.get('module')),
    }
    builder = builders.get(lesson_type)
    return builder() if builder else {}

def _build_questions(post_data):
    questions_raw = post_data.getlist('question[]')
    options_raw   = post_data.getlist('options[]')
    answers_raw   = post_data.getlist('answer[]')
    questions = []
    for i, q in enumerate(questions_raw):
        options = [o.strip() for o in options_raw[i].split('\n') if o.strip()]
        questions.append({
            'question': q,
            'options':  options,
            'answer':   int(answers_raw[i])
        })
    return {'questions': questions}

def _build_pdf(files, module):
    pdf = files.get('pdf') if files else None
    if not pdf or not module: 
        return {'url': ''}
    
    absolute_path = os.path.join('pdfs', f'module_{module}', pdf.name)
    path = default_storage.save(absolute_path, pdf)
    return {'url': path}