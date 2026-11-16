"""Interest catalog: each interest has a list of follow-up topics for onboarding."""

CATALOG: dict[str, list[str]] = {
    "news": ["world", "politics", "science", "health"],
    "sports": ["NFL", "NBA", "soccer", "F1"],
    "fashion": ["menswear", "womenswear", "streetwear", "luxury"],
    "tech": ["AI", "web dev", "gadgets", "startups"],
    "finance": ["markets", "crypto", "personal finance"],
    "cars": ["EVs", "sports cars", "industry"],
    "wearables": ["smartwatches", "fitness trackers", "AR glasses"],
}
