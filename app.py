from flask import Flask, render_template, request, jsonify
from models.extractive import ExtractiveTextSummarizer
from models.abstractive import AbstractiveTextSummarizer

"""
Text Summarizer Web Application
Author: Shahd Mohamed
GitHub: https://github.com/ShahdMohamed10
LinkedIn: https://www.linkedin.com/in/shahd-mohamed-123a68277/
"""

app = Flask(__name__)

# Initialize summarizers
extractive_summarizer = ExtractiveTextSummarizer()
abstractive_summarizer = AbstractiveTextSummarizer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.json
        text = data.get('text', '')
        method = data.get('method', 'both')
        ratio = float(data.get('ratio', 0.3))
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        result = {}
        
        try:
            if method in ['extractive', 'both']:
                result['extractive'] = extractive_summarizer.summarize(text, ratio=ratio)
            
            if method in ['abstractive', 'both']:
                result['abstractive'] = abstractive_summarizer.summarize(text, ratio=ratio)
            
            return jsonify(result)
        except Exception as e:
            app.logger.error(f"Summarization error: {str(e)}")
            return jsonify({'error': f'Summarization failed: {str(e)}'}), 500
    except Exception as e:
        app.logger.error(f"Request processing error: {str(e)}")
        return jsonify({'error': f'Request processing failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)