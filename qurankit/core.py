from __future__ import annotations

import json
import os
import random
import warnings
from collections import Counter, defaultdict
from typing import Any, Dict, List, Optional, Sequence
from urllib.request import Request, urlopen

from .config import (
    FEATURE_FIELDS,
    HIDDEN_FIELDS,
    TAFSIR_FIELDS,
    TRANSLATION_FIELDS,
    _DEFAULT_DATA_URL,
)

Ayah = Dict[str, Any]


class QuranKit:
    """Query-first toolkit for Quranic text, morphology, translations, and patterns.

    Normal methods return only the requested feature. QuranKit does not expose
    a public dataframe/export/full-json interface.

    Example:
        >>> from qurankit import QuranKit
        >>> q = QuranKit()
        >>> q.get_ayah(2, 255)
        >>> q.get_roots(2, 255)
        >>> q.get_translation(2, 255, lang="en")
    """

    def __init__(
        self,
        *,
        update: bool = False,
        use_sample_if_missing: bool = True,
        _data_url: Optional[str] = None,
        _local_path: Optional[str | os.PathLike[str]] = None,
    ) -> None:
        # Public use is QuranKit().
        # The full dataset is downloaded into memory only. It is not written to the user's disk.
        # _data_url and _local_path are internal/testing hooks.
        self._data_url = _data_url or _DEFAULT_DATA_URL

        if _local_path is not None:
            self._records = self._load_json_file(_local_path)
        else:
            try:
                self._records = self._download_json_to_memory(self._data_url)
            except Exception as exc:  # pragma: no cover
                if not use_sample_if_missing:
                    raise RuntimeError("Could not load the QuranKit dataset into memory.") from exc
                warnings.warn(
                    "Full QuranKit dataset was not downloaded. Loading bundled sample data into memory only.",
                    RuntimeWarning,
                )
                sample_path = os.path.join(os.path.dirname(__file__), "data", "sample.json")
                self._records = self._load_json_file(sample_path)
        self._index: Dict[tuple[int, int], Ayah] = {
            (int(x["sura"]), int(x["ayah"])): x for x in self._records
        }

    @staticmethod
    def _validate_dataset(data: Any) -> List[Ayah]:
        if not isinstance(data, list):
            raise ValueError("QuranKit dataset must be a list of ayah objects.")
        return data

    @classmethod
    def _load_json_file(cls, path: str | os.PathLike[str]) -> List[Ayah]:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls._validate_dataset(data)

    @classmethod
    def _download_json_to_memory(cls, url: str) -> List[Ayah]:
        req = Request(url, headers={"User-Agent": "qurankit/0.4.0"})
        with urlopen(req, timeout=120) as response:  # nosec B310
            content = response.read()
        data = json.loads(content.decode("utf-8"))
        return cls._validate_dataset(data)

    def _record(self, sura: int, ayah: int) -> Optional[Ayah]:
        return self._index.get((int(sura), int(ayah)))

    @staticmethod
    def _ayah_view(item: Ayah) -> Ayah:
        """Minimal ayah view: no morphology, no translations, no tafsir."""
        return {
            "sura": item.get("sura"),
            "ayah": item.get("ayah"),
            "sura_ar": item.get("sura_ar"),
            "sura_en": item.get("sura_en"),
            "ayatext_nt": item.get("ayatext_nt"),
        }

    @staticmethod
    def _search_view(item: Ayah, *, matched: Any = None, field: Optional[str] = None) -> Ayah:
        out = QuranKit._ayah_view(item)
        if matched is not None:
            out["matched"] = matched
        if field is not None:
            out["field"] = field
        return out

    @staticmethod
    def _limit(items: List[Any], limit: int) -> List[Any]:
        if limit is None or limit < 0:  # type: ignore[unreachable]
            return items
        return items[:limit]

    # -------------------------
    # Basic metadata
    # -------------------------
    def count_ayahs(self) -> int:
        """Return the number of loaded ayahs."""
        return len(self._records)

    def stats(self) -> Dict[str, Any]:
        """Return aggregate dataset statistics, not the dataset itself."""
        surahs = {int(x.get("sura", 0)) for x in self._records}
        roots = set()
        lemmas = set()
        for x in self._records:
            roots.update(r for r in (x.get("root_ar") or []) if r and r != "ـ")
            lemmas.update(l for l in (x.get("lemma_ar") or []) if l)
        return {
            "surahs": len(surahs),
            "ayahs": len(self._records),
            "languages": self.available_languages(),
            "roots": len(roots),
            "lemmas": len(lemmas),
        }

    def available_languages(self) -> List[str]:
        """List available translation language codes."""
        langs = set()
        for item in self._records[:50]:
            for key in item.keys():
                if key.endswith("_ayatext") and key not in {"ayatext", "ayatext_nt"}:
                    langs.add(key.replace("_ayatext", ""))
        return sorted(langs)

    def random_ayah(self) -> Ayah:
        """Return one random ayah in minimal form."""
        return self._ayah_view(random.choice(self._records))

    # -------------------------
    # Ayah and surah text
    # -------------------------
    def get_ayah(self, sura: int, ayah: int) -> Optional[Ayah]:
        """Return only the ayah text and reference."""
        item = self._record(sura, ayah)
        return None if item is None else self._ayah_view(item)

    def get_surah(self, sura: int, *, limit: Optional[int] = None) -> List[Ayah]:
        """Return ayah text/reference list for one surah only."""
        items = [self._ayah_view(x) for x in self._records if int(x.get("sura", -1)) == int(sura)]
        return items if limit is None else items[:limit]

    def get_ayah_text(self, sura: int, ayah: int, *, normalized: bool = True) -> Optional[str]:
        """Return only the ayah text string."""
        item = self._record(sura, ayah)
        if item is None:
            return None
        return item.get("ayatext_nt" if normalized else "ayatext")

    # -------------------------
    # Feature-specific getters
    # -------------------------
    def get_words(self, sura: int, ayah: int, *, normalized: bool = True) -> Optional[List[str]]:
        item = self._record(sura, ayah)
        return None if item is None else list(item.get("words_nt" if normalized else "words") or [])

    def get_roots(self, sura: int, ayah: int) -> Optional[List[str]]:
        item = self._record(sura, ayah)
        return None if item is None else list(item.get("root_ar") or [])

    def get_lemmas(self, sura: int, ayah: int) -> Optional[List[str]]:
        item = self._record(sura, ayah)
        return None if item is None else list(item.get("lemma_ar") or [])

    def get_pos(self, sura: int, ayah: int, *, arabic: bool = False) -> Optional[List[str]]:
        item = self._record(sura, ayah)
        return None if item is None else list(item.get("pos_ar" if arabic else "pos") or [])

    def get_morph_tags(self, sura: int, ayah: int) -> Optional[List[Any]]:
        item = self._record(sura, ayah)
        return None if item is None else list(item.get("morph_tags") or [])

    def get_analysis(self, sura: int, ayah: int) -> Optional[List[Any]]:
        item = self._record(sura, ayah)
        return None if item is None else list(item.get("analyses") or [])

    def word_analysis(self, sura: int, ayah: int) -> Optional[List[Dict[str, Any]]]:
        """Return aligned word-level analysis for one ayah only."""
        item = self._record(sura, ayah)
        if item is None:
            return None
        words = item.get("words_nt") or item.get("words") or []
        rows = []
        for i, word in enumerate(words):
            rows.append({
                "word_index": i + 1,
                "word": word,
                "word_original": _safe_index(item.get("words"), i),
                "word_translation": _safe_index(item.get("trans"), i),
                "pos": _safe_index(item.get("pos"), i),
                "pos_ar": _safe_index(item.get("pos_ar"), i),
                "lemma_ar": _safe_index(item.get("lemma_ar"), i),
                "root_ar": _safe_index(item.get("root_ar"), i),
                "analysis": _safe_index(item.get("analyses"), i),
                "morph_tags": _safe_index(item.get("morph_tags"), i),
            })
        return rows

    # -------------------------
    # Translations and tafsir only on request
    # -------------------------
    def get_translation(self, sura: int, ayah: int, *, lang: str = "en") -> Optional[Dict[str, Any]]:
        """Return one selected translation only."""
        item = self._record(sura, ayah)
        if item is None:
            return None
        return {
            **self._ayah_view(item),
            "lang": lang,
            "translation": item.get(f"{lang}_ayatext", ""),
        }

    def get_translations(self, sura: int, ayah: int, *, langs: Sequence[str] | None = None) -> Optional[Dict[str, Any]]:
        """Return selected translations only."""
        item = self._record(sura, ayah)
        if item is None:
            return None
        langs = list(langs) if langs is not None else self.available_languages()
        return {
            **self._ayah_view(item),
            "translations": {lang: item.get(f"{lang}_ayatext", "") for lang in langs},
        }

    def get_tafsir(self, sura: int, ayah: int, *, source: str = "muyassar") -> Optional[Dict[str, Any]]:
        """Return selected tafsir only. Supported: muyassar, jalalayn."""
        item = self._record(sura, ayah)
        if item is None:
            return None
        if source not in TAFSIR_FIELDS:
            raise ValueError(f"Unsupported tafsir source: {source}. Use one of {TAFSIR_FIELDS}.")
        return {**self._ayah_view(item), "source": source, "tafsir": item.get(source, "")}

    # -------------------------
    # Search methods: compact only
    # -------------------------
    def search_text(self, query: str, *, limit: int = 20) -> List[Ayah]:
        q = query.strip().lower()
        matches = [x for x in self._records if q in str(x.get("ayatext_nt", "")).lower()]
        return [self._search_view(x, matched=query, field="ayatext_nt") for x in matches[:limit]]

    def search_word(self, word: str, *, limit: int = 20) -> List[Ayah]:
        matches = [x for x in self._records if word in (x.get("words_nt") or [])]
        return [self._search_view(x, matched=word, field="words_nt") for x in matches[:limit]]

    def search_root(self, root: str, *, limit: int = 20) -> List[Ayah]:
        matches = [x for x in self._records if root in (x.get("root_ar") or [])]
        return [self._search_view(x, matched=root, field="root_ar") for x in matches[:limit]]

    def search_lemma(self, lemma: str, *, limit: int = 20) -> List[Ayah]:
        matches = [x for x in self._records if lemma in (x.get("lemma_ar") or [])]
        return [self._search_view(x, matched=lemma, field="lemma_ar") for x in matches[:limit]]

    def search_pos(self, pos: str, *, limit: int = 20) -> List[Ayah]:
        matches = [x for x in self._records if pos in (x.get("pos") or [])]
        return [self._search_view(x, matched=pos, field="pos") for x in matches[:limit]]

    def search_translation(self, query: str, *, lang: str = "en", limit: int = 20) -> List[Ayah]:
        field = f"{lang}_ayatext"
        q = query.strip().lower()
        matches = [x for x in self._records if q in str(x.get(field, "")).lower()]
        return [
            {**self._search_view(x, matched=query, field=field), "matched_translation": x.get(field, "")}
            for x in matches[:limit]
        ]

    # -------------------------
    # Pattern discovery: compact examples only
    # -------------------------
    def find_repeated_root_orders(self, *, min_occurrences: int = 2, limit: int = 20) -> List[Dict[str, Any]]:
        groups: Dict[str, List[Ayah]] = defaultdict(list)
        for item in self._records:
            roots = [r for r in (item.get("root_ar") or []) if r and r != "ـ"]
            signature = " | ".join(roots)
            if signature:
                groups[signature].append(item)

        output = []
        for signature, verses in groups.items():
            if len(verses) >= min_occurrences:
                output.append({
                    "root_order_signature": signature,
                    "count": len(verses),
                    "examples": [self._ayah_view(v) for v in verses[:5]],
                })
        output.sort(key=lambda x: x["count"], reverse=True)
        return output[:limit]

    def root_frequency(self, *, limit: int = 20) -> List[Dict[str, Any]]:
        counter: Counter[str] = Counter()
        for item in self._records:
            counter.update(r for r in (item.get("root_ar") or []) if r and r != "ـ")
        return [{"root": root, "count": count} for root, count in counter.most_common(limit)]


def _safe_index(values: Any, index: int) -> Any:
    if isinstance(values, list) and index < len(values):
        return values[index]
    return None
