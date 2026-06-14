# Dataset Information

QuranKit uses a hidden default dataset URL configured inside the package.

Users do not need to pass the URL:

```python
from qurankit import QuranKit
q = QuranKit()
```

The full dataset is downloaded into memory when QuranKit starts. QuranKit does not write the full dataset to the user's local disk. The public API is query-first and does not expose a full dataset export, dataframe export, or JSON dump method.
