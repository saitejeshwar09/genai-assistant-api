def generate_summary(text, max_sentences=5):
    sentences = text.replace("\n", " ").split(". ")
    meaningful = [s.strip() for s in sentences if len(s.strip()) > 30]
    summary = ". ".join(meaningful[:max_sentences]) + "."
    return summary if summary.strip() else text[:300]
