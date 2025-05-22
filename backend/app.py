from flask import Flask, request, jsonify
from transformers import BertTokenizer, BertForSequenceClassification
import torch

app = Flask(__name__)

# Muat model IndoBERT
tokenizer = BertTokenizer.from_pretrained('indolem/indobert-base-uncased')
model = BertForSequenceClassification.from_pretrained('indolem/indobert-base-uncased')

# Fungsi untuk menganalisis sentimen
def analyze_sentiment(text):
    # Tokenisasi input
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    
    # Prediksi sentimen
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
    
    # Ambil probabilitas dari logit (kelas 0 = Negatif, kelas 1 = Positif)
    sentiment = torch.argmax(logits, dim=1).item()
    
    if sentiment == 1:
        return "Positif"
    else:
        return "Negatif"

# Endpoint untuk analisis sentimen
@app.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment_api():
    data = request.json
    text = data['text']
    sentiment = analyze_sentiment(text)
    return jsonify({'sentiment': sentiment})

if __name__ == '__main__':
    app.run(debug=True)
