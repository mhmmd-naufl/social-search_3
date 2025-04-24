def analisis_komentar (text: str) -> str:
    if "bagus" in text or "keren" in text:
        return "positive"
    elif "jelek" in text or "buruk" in text:
        return "negative"
    else:
        return "neutral"
