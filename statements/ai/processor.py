from langdetect import detect
from transformers import pipeline
from keybert import KeyBERT
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Turkish Sentiment Analysis Model
sentiment_model = pipeline(
    "sentiment-analysis",
    model="savasy/bert-base-turkish-sentiment-cased"
)


# ✅ Multiple summarizer options with fallbacks
def initialize_summarizer():
    """Initialize summarizer with multiple fallbacks"""
    summarizer_options = [
        {
            "model": "ozcangundes/mt5-small-turkish-summarization",
            "use_fast": False,
            "name": "Turkish MT5 (slow tokenizer)"
        },
        {
            "model": "csebuetnlp/mT5_multilingual_XLSum",
            "use_fast": False,
            "name": "Multilingual MT5"
        },
        {
            "model": "facebook/bart-large-cnn",
            "use_fast": True,
            "name": "English BART (fallback)"
        }
    ]

    for option in summarizer_options:
        try:
            logger.info(f"Trying to load {option['name']}...")
            summarizer = pipeline(
                "summarization",
                model=option["model"],
                use_fast=option["use_fast"]
            )
            logger.info(f"Successfully loaded {option['name']}")
            return summarizer
        except Exception as e:
            logger.warning(f"Failed to load {option['name']}: {e}")

    logger.error("All summarizer options failed!")
    return None


# Initialize summarizer
summarizer = initialize_summarizer()

# ✅ Turkish-compatible KeyBERT
kw_model = KeyBERT(model='dbmdz/bert-base-turkish-cased')


def analyze_statement(statement_text):
    language = detect(statement_text)
    sentiment = None
    summary = None
    keywords = []

    # Temizleme
    cleaned_text = statement_text.replace("\r\n", " ").strip()

    # Duygu analizi
    try:
        sentiment_result = sentiment_model(cleaned_text[:512])
        sentiment = sentiment_result[0]['label'].upper()
    except Exception as e:
        sentiment = f"Duygu analizi başarısız: {str(e)}"
        logger.error(f"Sentiment analysis failed: {e}")

    # Özet
    if summarizer:
        try:
            # Determine max input length based on model
            max_input_length = 512
            input_text = cleaned_text[:max_input_length] if len(cleaned_text) > max_input_length else cleaned_text

            summary_result = summarizer(
                input_text,
                max_length=100,
                min_length=40,
                do_sample=False,
                truncation=True
            )
            summary = summary_result[0]['summary_text']
        except Exception as e:
            summary = f"Özetleme başarısız: {str(e)}"
            logger.error(f"Summarization failed: {e}")
    else:
        summary = "Özetleme modeli yüklenemedi"

    # Anahtar kelimeler
    try:
        keywords_result = kw_model.extract_keywords(
            cleaned_text,
            keyphrase_ngram_range=(1, 2),
            stop_words='turkish',
            top_n=5
        )
        keywords = [kw[0] for kw in keywords_result]
    except Exception as e:
        keywords = [f"Anahtar kelime çıkarımı başarısız: {str(e)}"]
        logger.error(f"Keyword extraction failed: {e}")

    return {
        "language": language,
        "sentiment": sentiment,
        "summary": summary,
        "keywords": keywords,
    }