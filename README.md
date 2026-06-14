# QuranKit

[![PyPI version](https://img.shields.io/pypi/v/qurankit.svg)](https://pypi.org/project/qurankit/)
[![Python](https://img.shields.io/pypi/pyversions/qurankit.svg)](https://pypi.org/project/qurankit/)
[![License](https://img.shields.io/github/license/alshargi/qurankit.svg)](LICENSE)

A powerful Python toolkit for Quranic text retrieval, linguistic analysis, morphology, root and lemma search, translations, tafsir access, and computational Quran research.

---

## Installation

```bash
pip install qurankit
```
## Why QuranKit?

QuranKit provides a unified Python interface for Quranic text, morphology, roots, lemmas, translations, tafsir, and computational analysis workflows.



---

## Quick Start

```python
from qurankit import QuranKit

q = QuranKit()

print(q.stats())

print(q.get_ayah(1, 1))

print(q.get_translation(2, 255, lang="en")["translation"])

```

---

## Features

### Quran Text

* Retrieve verses by surah and ayah
* Random verse generation
* Verse metadata access
* Compact response format

### Linguistic Analysis

* Word tokenization
* Root extraction
* Lemma extraction
* POS tagging
* Morphological feature access
* Full word-level analysis

### Search Engine

* Search Quran text
* Search words
* Search roots
* Search lemmas
* Search POS tags
* Translation search

### Translations

* Multiple language support
* Single translation retrieval
* Multi-translation retrieval
* Translation search

### Tafsir

* Al-Muyassar
* Al-Jalalayn
* On-demand retrieval

### Research & Analytics

* Root frequency analysis
* Repeated root-order discovery
* Pattern mining
* Statistical summaries
* Research-oriented querying

---

## Statistics

```python
q.stats()
```

---

## Verse Retrieval

```python
ayah = q.get_ayah(1, 1)
print(ayah)
```

Output:

```python
{
    "sura": 1,
    "ayah": 1,
    "sura_ar": "الفاتحة",
    "sura_en": "Al-Fātiḥah",
    "ayatext_nt": "بسم الله الرحمن الرحيم"
}
```

---

## Linguistic Features

```python
q.get_words(2, 255)

q.get_roots(2, 255)

q.get_lemmas(2, 255)

q.get_pos(2, 255)

q.get_morph_tags(2, 255)

q.get_analysis(2, 255)

q.word_analysis(2, 255)
```

---

## Search

### Text Search

```python
q.search_text("الله", limit=5)
```

### Word Search

```python
q.search_word("جنة", limit=5)
```

### Root Search

```python
q.search_root("رحم", limit=5)
```

### Lemma Search

```python
q.search_lemma("ٱللَّه", limit=5)
```

### POS Search

```python
q.search_pos("V", limit=5)
```

---

## Translations

List available languages:

```python
q.available_languages()
```

Retrieve a translation:

```python
q.get_translation(2, 255, lang="en")
```

Retrieve multiple translations:

```python
q.get_translations(
    1,
    1,
    langs=["en", "tr", "de"]
)
```

Search translations:

```python
q.search_translation(
    "mercy",
    lang="en",
    limit=5
)
```

---

## Tafsir

### Al-Muyassar

```python
q.get_tafsir(
    1,
    1,
    source="muyassar"
)
```

### Al-Jalalayn

```python
q.get_tafsir(
    1,
    1,
    source="jalalayn"
)
```

---

## Pattern Discovery

Repeated root-order patterns:

```python
q.find_repeated_root_orders(
    min_occurrences=2,
    limit=10
)
```

Root frequency:

```python
q.root_frequency(limit=20)
```

---

## Random Verse

```python
q.random_ayah()
```

---

## Example Research Workflow

```python
from qurankit import QuranKit

q = QuranKit()

verses = q.search_root("رحم", limit=10)

for verse in verses:
    print(
        verse["sura"],
        verse["ayah"],
        verse["ayatext_nt"]
    )
```

---

## Design Philosophy

QuranKit follows a query-first architecture designed for research and analysis.

Core principles:

* Lightweight API
* Focused retrieval
* Fast search
* Memory-efficient access
* Research-oriented workflows
* No API key required

---

## License

MIT License

---

## Citation - Author

```text
QuranKit: Python Toolkit for Computational Quran Analysis
Author: Dr. Faisal Alshargi
GitHub: https://github.com/alshargi/qurankit
PyPI: https://pypi.org/project/qurankit/
```

ثم
