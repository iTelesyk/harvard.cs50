import pytest
from pagerank import transition_model, sample_pagerank
SAMPLES = 10000

corpus = {
    "1.html": {"2.html", "3.html"},
    "2.html": {"3.html"},
    "3.html": {"2.html"}
}
page = "1.html"
damping_factor = 0.85

@pytest.mark.parametrize(
    "key,expected",
    [
        ("1.html", 0.05),
        ("2.html", 0.475),
        ("3.html", 0.475),
    ]
)
def test_transition_model_example_param(key, expected):
    result = transition_model(corpus, page, damping_factor)
    assert result[key] == pytest.approx(expected), (
        f"Mismatch for {key}: got {result[key]}, expected {expected}"
    )


def test_sample_pagerank_corpus_range():
    corpus = {'1': {'2'}, '2': {'3', '1'}, '3': {'2', '4'}, '4': {'2'}}
    damping_factor = 0.85

    pr = sample_pagerank(corpus, damping_factor, SAMPLES)
    assert 0.16991 <= pr['1'] <= 0.26991, f"pagerank for '1' out of range: got {pr['1']}"
