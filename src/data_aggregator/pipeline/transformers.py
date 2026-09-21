from data_aggregator.pipeline import pipeline


def transform_response(
    response: pipeline.StageInput,
) -> pipeline.StageOutput:
    return response