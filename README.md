# Phishing Email Detection System

A machine learning-based system for detecting phishing emails using BERT model and a modern UI built with CustomTkinter.

## Features

- Real-time phishing email detection
- Modern and responsive UI with dark/light mode
- FastAPI backend for model inference
- BERT-based model for accurate predictions
- Prediction history tracking

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Phishing_Email_Detection_System.git
cd Phishing_Email_Detection_System
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:

Start the FastAPI backend:
```bash
uvicorn main:app --reload
```

In a separate terminal, run the UI:
```bash
python UI.py
```

## Project Structure

- `main.py` - FastAPI backend for model inference
- `UI.py` - CustomTkinter-based user interface
- `model.safetensors` - Trained BERT model weights
- `config.json` - Model configuration
- `tokenizer.json` - Tokenizer configuration
- `requirements.txt` - Python dependencies

## Technologies Used

- Python
- FastAPI
- PyTorch
- Transformers (BERT)
- CustomTkinter
- Uvicorn

## License

MIT License 