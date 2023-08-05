from __future__ import annotations

from explainaboard import TaskType
from explainaboard.metric import BIOF1ScoreConfig, MetricConfig
from explainaboard.processors.processor_registry import register_processor
from explainaboard.processors.sequence_labeling import SeqLabProcessor
from explainaboard.utils.span_utils import BIOSpanOps


@register_processor(TaskType.chunking)
class ChunkingProcessor(SeqLabProcessor):
    @classmethod
    def task_type(cls) -> TaskType:
        return TaskType.chunking

    @classmethod
    def default_metrics(
        cls, source_language=None, target_language=None
    ) -> list[MetricConfig]:
        return [BIOF1ScoreConfig(name='F1')]

    @classmethod
    def default_span_ops(cls) -> BIOSpanOps:
        return BIOSpanOps()
