from transformers import MarianMTModel, MarianTokenizer

# Model name (choose language pair)
model_name = "Helsinki-NLP/opus-mt-en-es"  # English to Spanish
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

def translate_text(text):
    # Tokenize input text
    inputs = tokenizer(text, return_tensors="pt", padding=True)
    
    # Generate translation
    translated = model.generate(**inputs)
    
    # Decode and return result
    result = tokenizer.decode(translated[0], skip_special_tokens=True)
    return result

if __name__ == "__main__":
    # Test the translation function
    input_text = "Hello, how are you?"
    output_text = translate_text(input_text)
    print("Original:", input_text)
    print("Translated:", output_text)
