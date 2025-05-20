import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from rag import RAGSystem
import fitz  # PyMuPDF for PDF handling

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max file size

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize RAG system
rag_system = RAGSystem()

def allowed_file(filename):
    """Check if file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

def pdf_to_text(pdf_path):
    """Convert PDF to text"""
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error converting PDF to text: {str(e)}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Route for uploading PDFs and training the RAG system"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Save the PDF file
        filename = secure_filename(file.filename)
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(pdf_path)
        
        # Convert PDF to text
        text_content = pdf_to_text(pdf_path)
        if not text_content:
            return jsonify({'error': 'Failed to extract text from PDF'}), 400
            
        # Save text to data directory
        text_filename = f"{os.path.splitext(filename)[0]}.txt"
        rag_system.save_file(text_content, text_filename)
        
        # Train the RAG system
        success = rag_system.train()
        
        if success:
            return jsonify({
                'message': 'File uploaded and RAG system trained successfully',
                'filename': filename
            })
        else:
            return jsonify({'error': 'Failed to train RAG system'}), 500
    
    return jsonify({'error': 'File type not allowed. Please upload PDF files.'}), 400

@app.route('/query', methods=['POST'])
def query():
    """Route for querying the RAG system"""
    data = request.get_json()
    
    if not data or 'query' not in data:
        return jsonify({'error': 'No query provided'}), 400
    
    query_text = data['query']
    k = data.get('k', 5)  # Default to retrieving 5 documents
    
    # Query the RAG system
    result = rag_system.query(query_text, k=k)
    
    return jsonify(result)

@app.route('/clear', methods=['POST'])
def clear_data():
    """Route for clearing all data"""
    success = rag_system.clear_data()
    
    if success:
        # Also clear uploaded PDFs
        for file in os.listdir(app.config['UPLOAD_FOLDER']):
            if file.endswith('.pdf'):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
                
        return jsonify({'message': 'All data cleared successfully'})
    else:
        return jsonify({'error': 'Failed to clear data'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)