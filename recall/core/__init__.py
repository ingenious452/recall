from pathlib import Path
from typing import Optional

from recall.core.service import RecallOrchestrator


def get_orchestrator():
    return RecallOrchestrator.factory()


def init_service(db_file: Optional[Path], logs_dir: Optional[Path]):
    return RecallOrchestrator.init_recall(db_file, logs_dir)


__all__ = ["get_orchestrator", "init_service"]