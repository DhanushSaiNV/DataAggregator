# DataAggregator

A Python practice project that fetches, validates, and displays live data from multiple public APIs through a composable pipeline.

Built to explore: **Pydantic**, **abstract base classes**, **custom decorators**, **exception hierarchies**, **the pipeline pattern**, and **rich terminal output**.

---

## What It Does

Pulls live data from three sources simultaneously, runs each response through a configurable pipeline (validate → transform), and pretty-prints the result as a styled tree in the terminal.

| Source | API | Data |
|---|---|---|
| `WeatherSource` | Open-Meteo (free, no key) | Temperature, humidity, rain, day/night |
| `CountriesSource` | REST Countries v5 | Official name, capitals, region, currencies, languages |
| `CoinSource` | CoinGecko Demo | Bitcoin price, 24h/7d/30d/200d/1y % changes |

---

## Project Structure

```
src/data_aggregator/
├── __main__.py          # Entry point — wires sources + pipeline and runs
├── data_aggregator.py   # DataAggregator class: fetch → transform → display
│
├── domain/
│   ├── models.py        # Pydantic models: Raw*, Validated*, response hierarchy
│   ├── exceptions.py    # Typed exception hierarchy (AggregatorError subtree)
│   ├── decorators.py    # @parser decorator — wraps ValidationError uniformly
│   └── cli.py           # Rich-based recursive tree renderer (display function)
│
├── sources/
│   ├── data_source.py   # Abstract base: fetch() + parse()
│   ├── weather_source.py
│   ├── countries_source.py
│   └── coin_source.py
│
├── pipeline/
│   ├── pipeline.py      # Pipeline, PipelineStage (VALIDATE, TRANSFORM), PipelineState
│   └── transformers.py  # transform_response — placeholder, extend here
│
├── shared/
│   └── key_parser.py    # Recursive dict key extractor
│
└── tests/
    ├── test_pipeline.py
    ├── test_coin_source.py
    ├── test_countries_source.py
    ├── test_weather_source.py
    └── sample_userflow.py
```

---

## Setup

**Requirements:** Python 3.12+

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# 2. Install the package with dev dependencies
pip install -e ".[dev]"
```

**Environment variables** — create a `.env` file in the project root:

```env
COINGECKO_API_KEY=your_demo_key_here
REST_COUNTRIES_API_KEY=your_key_here
```

> A free CoinGecko Demo API key can be obtained at [coingecko.com](https://www.coingecko.com/en/api). The Open-Meteo weather source requires no key.

---

## Run

```bash
python -m data_aggregator
```

This fetches all three sources, validates the responses, and prints a colour-coded tree to the terminal for each one.

---

## How It Works

### 1. DataAggregator — the orchestrator

```python
DataAggregator(sources, pipeline_stages).fetch().transform().display()
```

- **`fetch()`** — iterates over each `DataSource` subclass, calls `.fetch().parse()`, and builds a `PipelineConfig` per source.
- **`transform()`** — runs each config through the `Pipeline`, collecting `PipelineState` outputs.
- **`display()`** — passes each output to `cli.display()` for rich tree rendering.

### 2. DataSource — the abstract contract

Every source implements two methods:

```python
class DataSource(ABC):
    def fetch(self, endpoint: str = "", *kwargs) -> Self: ...
    def parse(self, response_dict: dict | None = None) -> ResponseModel: ...
```

The `@parser` decorator on `parse()` intercepts Pydantic `ValidationError` and re-raises it as `ResponseValidationError` with full context (the dict that failed, the model it was tested against).

### 3. Pipeline — composable stages

```python
Pipeline(PipelineStage.VALIDATE, PipelineStage.TRANSFORM)
```

Stages are `Enum` values. The pipeline iterates them in order, passing a `PipelineState` object through each registered handler. Currently supports:

| Stage | What it does |
|---|---|
| `VALIDATE` | `model_validate()` from Raw → Validated Pydantic model |
| `TRANSFORM` | Calls `transform_response()` — a no-op pass-through by default |

To add a stage: add a new `PipelineStage` variant and register a handler in `STEP_REGISTRY`.

### 4. Models — two-tier Pydantic validation

Each source has a **Raw** model (loose, matches the API shape exactly) and a **Validated** model (strict, with field constraints, coercions, and cross-field checks). For example:

- `RawWeatherResponse` stores `timezone_b: bytes` and `is_day: float`
- `ValidatedWeatherResponse` decodes the bytes to `str`, coerces `is_day` to `bool`, parses Unix time to `datetime`, and enforces lat/lon bounds

### 5. Exception Hierarchy

```
AggregatorError
├── DataFetchError
│   ├── APIKeyError
│   ├── ResponseValidationError
│   └── InvalidSourceError
└── PipelineError
    ├── InvalidPipelineStageError
    ├── ValidationPipelineError
    └── InvalidTransformerError
```

All exceptions bubble up to `DataAggregator`, which catches each type and re-raises as `AggregatorError` with a clean message.

---

## Running Tests

```bash
pytest src/data_aggregator/tests/
```

> Note: most tests currently make live API calls. They serve as integration smoke tests rather than isolated unit tests.

---

## Python Concepts Practised

- Abstract base classes (`ABC`, `@abstractmethod`)
- Pydantic v2 — `BaseModel`, `field_validator`, `model_validator`, `ConfigDict`, `Annotated` constraints
- Custom decorator (`@parser`) using `functools.wraps`
- Typed exception hierarchy
- The pipeline / chain-of-responsibility pattern
- `Enum` + `auto()` for stage definitions
- `dataclass` for value objects (`PipelineConfig`, `PipelineState`)
- Fluent / method-chaining API (`fetch().transform().display()`)
- `rich` library for terminal tree rendering
- `python-dotenv` for environment variable management
- `src` layout with editable install (`pip install -e .`)
