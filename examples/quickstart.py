from qurankit import QuranKit

q = QuranKit()

print(q.stats())
print(q.get_ayah(1, 1))
print(q.get_roots(1, 1))
print(q.search_root("رحم", limit=3))
print(q.get_translation(2, 255, lang="en"))
print(q.word_analysis(1, 1))
