VALIDATE=1
TRANSFORM, res, SOURCE, MODEL = 1,1,1,1

da = DataAggregator()


pipeline = da.create_pipeline(
    stages=[VALIDATE, TRANSFORM]
)

pipeline.run(
    response=res, 
    source=SOURCE,
    model=MODEL
)

# TODO: 
# 1. Complete implementing Pipeline
    # - transform()
    # - run()
