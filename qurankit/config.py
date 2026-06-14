"""Internal configuration for QuranKit."""

from __future__ import annotations

CACHE_DIR_NAME = ".qurankit"
DATA_FILE_NAME = "quran_faisal.json"

# Hidden default dataset URL. Users can simply call QuranKit().
_DEFAULT_DATA_URL = "https://www.sanaa.ai/quran/qurandb/quran_faisal.json"

TRANSLATION_FIELDS = [
    "en_ayatext",
    "tr_ayatext",
    "de_ayatext",
    "ru_ayatext",
    "bn_ayatext",
    "nl_ayatext",
]

TAFSIR_FIELDS = ["jalalayn", "muyassar"]

# Fields never returned by default because each feature has its own getter.
FEATURE_FIELDS = [
    "words",
    "words_nt",
    "analyses",
    "morph_tags",
    "trans",
    "pos",
    "pos_ar",
    "lemma_ar",
    "root_ar",
]

HIDDEN_FIELDS = TRANSLATION_FIELDS + TAFSIR_FIELDS + FEATURE_FIELDS
