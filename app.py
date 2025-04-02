from flask import Flask, render_template, request, jsonify
import pandas as pd
from anonymize import anonymizeDataframe
from analysis import analyze_data
from groq_api import get_groq_response
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'csv'}


DATASET = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET'])
def index():
    return render_template('chat.html')

@app.route('/chat', methods=['GET'])
def chat():
    user_input = request.args.get('user_input')
    if not user_input:
        return "Hello, I am llmano, an AI to help you anonymize your data. Please upload your data as a CSV here."
    

    # Check if the dataset is loaded
    if DATASET is None:
        return "Please upload a CSV file first."
    

    anlaizedData = analyze_data(DATASET)
    
    # desired_k = 3
    # desired_l = 2
    # anonamizedData = anonymizeDataframe(DATASET, desired_k, desired_l)

    LLM_Prompt = f"{anlaizedData}\n\n{user_input}"

    print("\n\nLLM Prompt: ", LLM_Prompt)

    llm_response = get_groq_response(LLM_Prompt)

    print("\n\nLLM Response: ", llm_response)

    return llm_response
  

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'csv_file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['csv_file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.csv'):
        global DATASET
        df = pd.read_csv(file)
        DATASET = df
        return jsonify({'message': 'File uploaded successfully'}), 200

    return jsonify({'error': 'Invalid file format, please upload a CSV.'}), 400



if __name__ == '__main__':
    app.run(debug=True)
