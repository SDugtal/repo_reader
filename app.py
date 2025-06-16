from flask import Flask, render_template, request, send_from_directory
from document_generator import RepoDocumentGenerator
import os

app = Flask(__name__)
app.config['OUTPUT_DIR'] = 'output'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get filters from form
        filters = {
            'language': request.form.get('language'),
            'min_stars': int(request.form.get('min_stars')) if request.form.get('min_stars') else None
        }
        sort_by = request.form.get('sort_by', 'updated')
        
        # Generate report
        generator = RepoDocumentGenerator()
        report = generator.generate_all(output_dir=app.config['OUTPUT_DIR'], 
                                     filters=filters, 
                                     sort_by=sort_by)
        
        return render_template('report.html', 
                            report=report,
                            filters=filters,
                            sort_by=sort_by)
    
    return render_template('index.html')

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['OUTPUT_DIR'], filename)

if __name__ == '__main__':
    os.makedirs(app.config['OUTPUT_DIR'], exist_ok=True)
    app.run(debug=True)