import json
import logging
from pathlib import Path
from typing import Dict, Optional, Union

logger = logging.getLogger(__name__)


def get_k8s_metadata(metadata_dir: Union[str, Path] = None) -> Optional[Dict]:
    metadata = {}
    if not metadata_dir.exists():
        # TODO try to get from env vars?
        return

    for name in ('name', 'namespace'):
        path = metadata_dir / name
        if path.exists():
            with path.open() as f:
                metadata[name] = f.readline().strip()
    for name in ('labels', 'annotations'):
        path = metadata_dir / name
        if path.exists():
            with path.open() as f:
                lines = f.readlines()
                lines = (line.split('=', 1) for line in lines if line)
                metadata[name] = {
                    k.strip().replace('.', '-'): v.strip().strip('"')  # NOTE: elastic is not accepting keys with dots
                    for k, v in lines
                }
    return metadata


original_log_record_factory = logging.getLogRecordFactory()


def setup_logging_k8s_metadata(metadata_attr_name: str = None, metadata_dir: Union[str, Path] = None, dump=True):
    """
    Set up log record factory

    Set up custom factory which sets kubernetes metadata attribute into log
    record.

    Args:
        metadata_attr_name: Kubernetes metadata attribute name.
            Default: 'kubernetes'
        metadata_dir: Metadata directory. Default: '/etc/podinfo'
        dump: Whether to dump metadata to json
    """

    def log_record_factory(*args, **kwargs):
        record = original_log_record_factory(*args, **kwargs)
        setattr(record, metadata_attr_name or 'kubernetes', k8s_metadata)
        return record

    k8s_metadata = get_k8s_metadata(metadata_dir=Path(metadata_dir or '/etc/podinfo'))
    if dump:
        k8s_metadata = json.dumps(k8s_metadata)
    logging.setLogRecordFactory(log_record_factory)


def send_log():
    import logging.config
    from datetime import datetime
    import yaml

    setup_logging_k8s_metadata(metadata_dir='../eam-pmm-series-transformer/data/podinfo')

    logger = logging.getLogger(__name__)
    with open('logging.yml') as f:
        pass
        LOGGING = yaml.safe_load(f.read())
        # LOGGING['formatters']['fluent']['fill_missing_fmt_key'] = True
        # LOGGING['formatters']['fluent']['format']['kubernetes'] = '{kubernetes}'

    logging.config.dictConfig(LOGGING)
    try:
        raise Exception('Original exception.')
    except Exception as e:
        logger.exception(f'Some exception at {datetime.now()}')
    # logger.info(f'Test {datetime.now()}')
    # logger.error(f"Some exception at {datetime.now()}\nTraceback (most recent call last):\n  File \"/home/nz/dev/logging-k8s-metadata/logging_k8s_metadata/__init__.py\", line 62, in <module>\n    raise Exception('Original exception.')\nException: Original exception.")


if __name__ == '__main__':
    send_log()
