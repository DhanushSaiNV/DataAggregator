from dataclasses import asdict
from pprint import pprint

from data_aggregator.domain.models import ValidatedCoinResponse
from data_aggregator.pipeline.pipeline import (
    Pipeline,
    PipelineConfig,
    PipelineStage,
    PipelineState,
)
from data_aggregator.sources.coin_source import CoinSource

coinsource = CoinSource()

pipeline = Pipeline(PipelineStage.VALIDATE, PipelineStage.TRANSFORM)

raw_resp = coinsource.fetch().parse()

pipeline_config = PipelineConfig(raw_resp, CoinSource, ValidatedCoinResponse)

output_state: PipelineState = pipeline.run(pipeline_config)

pprint(asdict(output_state))
