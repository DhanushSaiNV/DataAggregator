VALIDATE=1
CLEAN, TRANSFORM, res, SOURCE, MODEL = 1,1,1,1,1

da = DataAggregator()

# bad: creation is independent of sources and responses
# pipeline = da.createpipeline(SOURCES, MODELS)

pipeline = da.create_pipeline(
    stages=[VALIDATE, CLEAN, TRANSFORM]
)

pipeline.run(
    response=res, 
    source=SOURCE,
    model=MODEL
)

