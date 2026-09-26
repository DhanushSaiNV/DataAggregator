# DataAggregator

A Python practice project that fetches, validates, and displays live data from multiple public APIs through a composable pipeline.

Built to explore: **Pydantic**, **abstract base classes**, **asyncio**, **custom decorators**, **exception hierarchies**, **the pipeline pattern**, and **rich terminal output**.

---

## What It Does

Pulls live data from three sources, runs each response through a configurable pipeline (validate → transform), and pretty-prints the result as a styled tree in the terminal.

Supports two execution modes — **async** (default, concurrent fetching via `asyncio.gather`) and **sync** (sequential, opt-in via a CLI flag).

| Source | API | Data |
|---|---|---|
| `WeatherSource` / `AsyncWeatherSource` | Open-Meteo (free, no key) | Temperature, humidity, rain, day/night |
| `CountriesSource` / `AsyncCountriesSource` | REST Countries v5 | Official name, capitals, region, currencies, languages |
| `CoinSource` / `AsyncCoinSource` | CoinGecko Demo | Bitcoin price, 24h/7d/30d/200d/1y % changes |

---

## Project Structure

```
src/data_aggregator/
├── __main__.py          # Entry point — argparse flag selects sync vs. async mode
├── data_aggregator.py   # DataAggregator (sync) + AsyncDataAggregator (async)
│
├── domain/
│   ├── models.py        # Pydantic models: Raw*, Validated*, response hierarchy
│   ├── exceptions.py    # Typed exception hierarchy (AggregatorError subtree)
│   ├── decorators.py    # @parser decorator — wraps ValidationError uniformly
│   └── cli.py           # Rich-based recursive tree renderer (display function)
│
├── sources/
│   ├── data_source.py   # Two ABCs: DataSource (sync) + AsyncDataSource (async)
│   ├── weather_source.py   # WeatherSource + AsyncWeatherSource
│   ├── countries_source.py # CountriesSource + AsyncCountriesSource (uses httpx)
│   └── coin_source.py      # CoinSource + AsyncCoinSource
│
├── pipeline/
│   ├── pipeline.py      # Pipeline, PipelineStage (VALIDATE, TRANSFORM), PipelineState
│   └── transformers.py  # transform_response — placeholder, extend here
│
├── shared/
│   └── key_parser.py    # Recursive dict key extractor
│
└── tests/
    ├── practice_asyncio.py      # asyncio.Queue producer/processor/consumer playground
    ├── test_aggregator.py       # Sync vs. async timing comparison
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
# Default — async mode (concurrent fetching, faster)
python -m data_aggregator

# Sync mode — sequential fetching
python -m data_aggregator --synchronous
```

Both modes print a response time after displaying results, so you can compare performance directly.

---

## How It Works

### 1. Two aggregator classes

`DataAggregator` and `AsyncDataAggregator` share the same pipeline and display logic but differ in how they fetch:

| Class | How it fetches |
|---|---|
| `DataAggregator` | Iterates sources sequentially, calls `source.fetch().parse()` |
| `AsyncDataAggregator` | Fires all `async fetch()` calls concurrently with `asyncio.gather`, then pipelines the results |

Both expose a single `.run(display=True)` method that internally calls fetch → transform → (optionally) display.

### 2. Dual DataSource ABCs

`data_source.py` now defines **two** abstract base classes:

```python
class DataSource(ABC):           # sync sources
    def fetch(...) -> Self: ...
    def parse(...) -> ResponseModel: ...

class AsyncDataSource(ABC):      # async sources
    async def fetch(...) -> Self: ...
    def parse(...) -> ResponseModel: ...  # parse stays sync
```

Every source ships in both flavours (e.g. `WeatherSource` / `AsyncWeatherSource`). The sync class carries an `async_version` class attribute pointing to its async counterpart.

The async `CountriesSource` switches from `requests` to **`httpx.AsyncClient`** for non-blocking HTTP.

### 3. CLI flag with argparse

`__main__.py` uses `argparse` to expose a `--synchronous` / `-s` flag. Without it, `AsyncDataAggregator` runs by default.

### 4. Pipeline — composable stages

```python
Pipeline(PipelineStage.VALIDATE, PipelineStage.TRANSFORM)
```

Stages are `Enum` values. The pipeline iterates them in order, passing a `PipelineState` object through each registered handler. Currently supports:

| Stage | What it does |
|---|---|
| `VALIDATE` | `model_validate()` from Raw → Validated Pydantic model |
| `TRANSFORM` | Calls `transform_response()` — a no-op pass-through by default |

To add a stage: add a new `PipelineStage` variant and register a handler in `STEP_REGISTRY`.

### 5. Models — two-tier Pydantic validation

Each source has a **Raw** model (loose, matches the API shape exactly) and a **Validated** model (strict, with field constraints, coercions, and cross-field checks). For example:

- `RawWeatherResponse` stores `timezone_b: bytes` and `is_day: float`
- `ValidatedWeatherResponse` decodes the bytes to `str`, coerces `is_day` to `bool`, parses Unix time to `datetime`, and enforces lat/lon bounds

### 6. Exception Hierarchy

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

All exceptions bubble up through the aggregator, which catches each type and re-raises as `AggregatorError` with a clean message.

---

## Running Tests

```bash
pytest src/data_aggregator/tests/
```

> Note: tests make live API calls — they are integration smoke tests, not isolated unit tests. `practice_asyncio.py` and `test_aggregator.py` can be run directly with `python` to observe timing output.

---

## Python Concepts Practised

- Abstract base classes (`ABC`, `@abstractmethod`)
- Pydantic v2 — `BaseModel`, `field_validator`, `model_validator`, `ConfigDict`, `Annotated` constraints
- Custom decorator (`@parser`) using `functools.wraps`
- Typed exception hierarchy
- The pipeline / chain-of-responsibility pattern
- `Enum` + `auto()` for stage definitions
- `dataclass` for value objects (`PipelineConfig`, `PipelineState`)
- **`asyncio`** — `async`/`await`, `asyncio.gather`, `asyncio.run`, `asyncio.Queue`
- **`httpx.AsyncClient`** for non-blocking HTTP
- **`argparse`** for CLI argument parsing
- `rich` library for terminal tree rendering
- `python-dotenv` for environment variable management
- `src` layout with editable install (`pip install -e .`)
