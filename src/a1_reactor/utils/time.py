from __future__ import annotations

import time
from contextlib import contextmanager
from typing import Callable, Iterator, Optional

@contextmanager
def timed(label: str, log: Optional[Callable[[str], None]] = None) -> Iterator[None]:
    start = time.time()
    try:
        yield
    finally:
        dt = (time.time() - start) * 1000
        msg = f"{label}: {dt:.1f}ms"
        if log:
            log(msg)
