import pytest

from readme.card.documents.document import CardDocumentsDocument


@pytest.mark.parametrize(
    ("size", "label"),
    [
        (0, "0"),
        (1023, "1023"),
        (1024, "1.0K"),
        (1025, "1.1K"),
        (10 * 1024, "10K"),
        (10 * 1024 + 1, "11K"),
        (5 * 1024 * 1024, "5.0M"),
    ],
)
def test_human_size_rounds_up_like_ls(size: int, label: str) -> None:
    assert CardDocumentsDocument.human_size(size) == label
