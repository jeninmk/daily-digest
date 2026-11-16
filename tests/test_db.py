from digest.db import Article, Store


def test_add_new_returns_only_unseen(tmp_path):
    store = Store(tmp_path / "t.db")
    a = Article(url="http://x/1", title="T", source="S", interest="news", published=None)
    assert store.add_new([a]) == [a]
    assert store.add_new([a]) == []
    assert store.count() == 1
    store.close()
