from qurankit import QuranKit


def test_basic_sample_loading():
    q = QuranKit(_local_path="qurankit/data/sample.json")
    assert q.count_ayahs() >= 1
    assert q.get_ayah(1, 1)["ayatext_nt"] == "بسم الله الرحمن الرحيم"
    assert isinstance(q.get_roots(1, 1), list)
    assert "translation" in q.get_translation(1, 1, lang="en")
    assert q.search_root("رحم", limit=1)
