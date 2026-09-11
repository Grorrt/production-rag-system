"""
Tests for the evaluation framework.
"""

from backend.app.system_evaluation.evaluation_metrics import RAGEvaluator
from backend.app.system_evaluation.golden_dataset import load_golden_dataset


class TestRAGEvaluator:
    def setup_method(self):
        self.evaluator = RAGEvaluator()

    def test_recall_at_k(self):
        retrieved = ["a", "b", "c", "d", "e"]
        relevant = ["a", "c"]
        result = self.evaluator._recall_at_k(retrieved, relevant, k=5)
        assert result == 1.0

    def test_recall_at_k_with_misses(self):
        retrieved = ["x", "y", "z"]
        relevant = ["a"]
        result = self.evaluator._recall_at_k(retrieved, relevant, k=3)
        assert result == 0.0

    def test_mean_reciprocal_rank(self):
        retrieved = ["x", "y", "a", "z"]
        relevant = ["a"]
        result = self.evaluator._mean_reciprocal_rank(retrieved, relevant)
        assert result == 1.0 / 3

    def test_precision_at_k(self):
        retrieved = ["a", "b", "c", "d", "e"]
        relevant = ["a", "b"]
        result = self.evaluator._precision_at_k(retrieved, relevant, k=5)
        assert result == 0.4

    def test_compute_retrieval_metrics(self):
        retrieved = ["a", "b", "c"]
        relevant = ["a"]
        metrics = self.evaluator.compute_retrieval_metrics(retrieved, relevant)
        assert "recall_at_5" in metrics
        assert "mrr" in metrics
        assert "precision_at_5" in metrics


class TestGoldenDataset:
    def test_dataset_has_samples(self):
        samples = load_golden_dataset()
        assert len(samples) > 0

    def test_samples_have_required_fields(self):
        samples = load_golden_dataset()
        for sample in samples:
            assert sample.question
            assert sample.ground_truth
            assert sample.expected_sources
            assert sample.category

    def test_dataset_covers_multiple_categories(self):
        samples = load_golden_dataset()
        categories = set(s.category for s in samples)
        assert len(categories) >= 2
