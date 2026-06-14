# QuranKit

**QuranKit** is a query-first Python toolkit for computational Quran analysis, providing structured access to Quranic text, morphology, roots, lemmas, translations, tafsir, and linguistic pattern discovery.

Developed by **Dr. Faisal Alshargi**.

---

## Features

* Quranic verse retrieval
* Root-based search
* Lemma-based search
* Word-level linguistic analysis
* POS tagging access
* Morphological feature access
* Multi-language translations
* Tafsir retrieval
* Root-order pattern discovery
* Frequency analysis
* Research-oriented querying
* Memory-only dataset loading

---

## Design Philosophy

QuranKit is designed around **feature-level access rather than dataset export**.

Users interact with the Quran through focused search and analysis functions instead of downloading or manipulating the complete dataset.

### Core Principles

* Returns only the requested information
* Compact results by default
* No API key required
* No remote inference
* Query-first architecture
* Memory-only dataset loading
* Translation and tafsir access only when explicitly requested

QuranKit intentionally does **not** provide:

```python
q.to_dataframe()
q.export_json()
q.export_dataset()
q.dump_all()
```

This keeps the package focused on analysis, exploration, and research rather than dataset replication.

---

## Installation

```bash
pip install qurankit
```

For development:

```bash
pip install -e .
```

---

## Quick Start

```python
from qurankit import QuranKit

q = QuranKit()

print(q.stats())

ayah = q.get_ayah(1, 1)
print(ayah)

results = q.search_root("رحم", limit=3)

translation = q.get_translation(2, 255, lang="en")
print(translation["translation"])
```

---

## Statistics

```python
q.stats()
```

Example:

```python
{
    "surahs": 114,
    "ayahs": 6236,
    "languages": 20,
    "roots": 1600,
    "lemmas": 14000
}
```

---

## Verse Retrieval

```python
q.get_ayah(1, 1)
```

Example output:

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

Retrieve individual linguistic layers without loading unnecessary information.

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

### Search Text

```python
q.search_text("الله", limit=5)
```

### Search Word

```python
q.search_word("جنة", limit=5)
```

### Search Root

```python
q.search_root("رحم", limit=5)
```

### Search Lemma

```python
q.search_lemma("ٱللَّه", limit=5)
```

### Search POS Tags

```python
q.search_pos("V", limit=5)
```

Search results remain compact and exclude long translations and tafsir content.

---

## Translations

List available languages:

```python
q.available_languages()
```

Retrieve a specific translation:

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

Search inside translations:

```python
q.search_translation(
    "mercy",
    lang="en",
    limit=5
)
```

---

## Tafsir

Retrieve tafsir only when requested.

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

Root frequency statistics:

```python
q.root_frequency(limit=20)
```

---

## Random Verse

```python
q.random_ayah()
```

---

## Dataset Handling

QuranKit ships with a minimal bundled sample dataset for testing and fallback purposes.

The complete Quran dataset is loaded from the internal default dataset source into memory only.

QuranKit does not intentionally persist the full dataset to local storage and does not provide dataset export utilities.

---

## Performance

```python
import time

start = time.time()

q = QuranKit()

print(
    "Load time:",
    round(time.time() - start, 2),
    "seconds"
)
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

## Disclaimer

QuranKit is intended for computational analysis, research, education, and software development.

It is not a source of religious rulings, legal opinions, or authoritative tafsir.

```
```

