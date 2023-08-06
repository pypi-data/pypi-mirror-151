import logging
from typing import Optional

from airflow.operators import BaseOperator
from airflow.utils.decorators import apply_defaults


class AnnotationPropagationOperator(BaseOperator):

    template_fields = ()
    ui_color = '#fee8f4'

    @apply_defaults
    def __init__(
        self,
        openlineage_conn_id: Optional[str] = None,
        *args,
        **kwargs
    ) -> None:
        super(AnnotationPropagationOperator, self).__init__(*args, **kwargs)
        self.openlineage_conn_id = openlineage_conn_id

    def execute(self, context):
        logging.info("Start propagating annotation")
