from a1_reactor.engine.windows import normalize_windows

def test_normalize_windows_merges():
    w = normalize_windows([(0.1, 0.5), (0.4, 0.9), (1.2, 1.3)], seconds=2.0)
    assert len(w) == 2
    assert w[0].start_s == 0.1
    assert w[0].end_s == 0.9
