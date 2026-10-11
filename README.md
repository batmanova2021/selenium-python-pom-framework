# Enterprise Selenium Python POM Framework

A production-grade, FAANG-caliber UI test automation framework built with **Python 3.12+**, **Selenium WebDriver 4**, **PyTest**, and **Allure**, managed with **[uv](https://docs.astral.sh/uv/)**.

Designed following Big Tech test engineering principles: strict Page Object / Component separation, zero POM assertions, 12-factor configuration, comprehensive static typing, structured observability, and CI/CD quality gates.

---

## Technology Stack

| Technology | Purpose |
| :--- | :--- |
| **Python 3.12+** | Language under test with full PEP 484 static typing |
| **[uv](https://docs.astral.sh/uv/)** | Extremely fast Python dependency & project manager |
| **[Selenium 4](https://www.selenium.dev/)** | Browser automation with built-in Selenium Manager |
| **[PyTest](https://docs.pytest.org/)** | Test runner, fixtures, markers, and parametrization |
| **[Allure](https://allurereport.org/)** | Interactive reporting with failure screenshots, logs, and `@allure.step` |
| **`pytest-rerunfailures`** | Automated retry policies for network & UI flakiness resilience |
| **`pytest-html`** | Self-contained standalone HTML test reports |
| **`ruff`** | Fast linting and PEP 8 formatting |
| **`pylint`** | Deep static code analysis (10.00 / 10 rating) |
| **`mypy`** | Strict static type checking |
| **GitHub Actions** | CI/CD pipeline with lint quality gates, multi-browser matrix, and report publishing |

---

## Architectural Highlights

- **Component Object Model (COM)**: Shared UI elements (e.g., [`HeaderComponent`](pages/components/header_component.py)) are isolated as reusable components and composed into page objects rather than duplicated across pages.
- **Strict Separation of Concerns**: Page Objects model state, user actions, and page queries (`get_title()`, `wait_for_search_results()`). Assertions live strictly inside test functions.
- **12-Factor Configuration**: Environment variables and default parameters are centralized in [`config.py`](config.py) using typed dataclasses with zero hardcoded URLs or timeouts in tests.
- **Observability**: Standard Python `logging` streams structured logs (`INFO`, `DEBUG`) through PyTest live CLI, paired with Allure step decorations (`@allure.step`).
- **Resilience Against Flakiness**: Anti-bot user-agent resolution, page load and script timeouts, plus automatic retries in CI (`--reruns 2 --reruns-delay 1`).

---

## Prerequisites

1. **Git**
2. **Python 3.12 or later** (managed automatically by `uv`)
3. **uv**:
   ```bash
   # macOS / Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   # Or via Homebrew
   brew install uv

   # Windows (PowerShell)
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```
4. **Google Chrome** or **Firefox** installed.
   *(Selenium Manager resolves drivers automatically; manual binary downloads are not needed).*
5. **Allure CLI** (for viewing reports):
   ```bash
   # macOS
   brew install allure

   # Windows (Scoop / Chocolatey)
   scoop install allure
   ```

---

## Setup

Clone the repository and synchronize the environment:

```bash
uv sync
```

---

## Configuration

Settings can be overridden via environment variables:

| Variable | Default | Description |
| :--- | :--- | :--- |
| `EBAY_BASE_URL` | `https://www.ebay.com` | Base URL under test |
| `SELENIUM_TIMEOUT` | `10.0` | Default explicit wait timeout (seconds) |
| `SELENIUM_PAGE_LOAD_TIMEOUT` | `30.0` | Maximum page load timeout (seconds) |
| `SELENIUM_SCRIPT_TIMEOUT` | `30.0` | Maximum asynchronous script timeout (seconds) |
| `SELENIUM_BROWSER` | `chrome` | Default browser (`chrome` or `firefox`) |
| `SELENIUM_HEADLESS` | `false` | Run headless by default (`true` / `false`) |

---

## Code Quality Gates

Run all static analysis tools before submitting pull requests:

```bash
# 1. Ruff linting
uv run ruff check .

# 2. Ruff format validation
uv run ruff format --check .

# 3. Pylint static analysis (enforces >= 8.0)
uv run pylint pages/ tests/ config.py --fail-under=8.0

# 4. Mypy static type checking
uv run mypy pages tests config.py
```

---

## Running Tests

### Standard Execution

```bash
# Run tests with visible Chrome browser
uv run pytest --browser=chrome

# Run tests in headless mode (recommended for CI)
uv run pytest --browser=chrome --headless

# Run tests in Firefox
uv run pytest --browser=firefox --headless
```

### Targeted Suites

```bash
# Smoke suite
uv run pytest -m smoketest --browser=chrome --headless

# Full regression suite
uv run pytest -m regressiontest --browser=chrome --headless

# Run tests with automatic retries for transient failures
uv run pytest -m smoketest --reruns 2 --reruns-delay 1 --headless

# Parallel test execution across CPU cores
uv run pytest -n auto --headless
```

---

## Test Reports

### Allure Reports

- **Serve live interactive report in your browser**:
  ```bash
  allure serve allure-results
  ```
- **Generate standalone static HTML report**:
  ```bash
  allure generate allure-results --clean -o allure-report
  ```
- **Open generated HTML report**:
  ```bash
  allure open allure-report
  ```

### PyTest HTML Report

Located at:
```text
reports/report.html
```

---

## CI/CD Pipeline (GitHub Actions)

Configured in [`.github/workflows/qa.yml`](.github/workflows/qa.yml):

1. **Quality Gate (`lint` job)**:
   - Enforces `ruff check`, `ruff format --check`, `pylint`, and `mypy`.
   - Tests do not execute if static analysis fails.
2. **Matrix Execution (`test` job)**:
   - Multi-browser matrix (`chrome`, `firefox`).
   - Runs **Smoke tests** on every push & pull request.
   - Runs **Regression tests** nightly at 02:00 UTC.
   - Applies flakiness retries (`--reruns 2 --reruns-delay 1`).
3. **Artifact Publishing**:
   - Publishes raw Allure results (`allure-results/`).
   - Generates and uploads Allure HTML report (`allure-report/`).
   - Publishes PyTest HTML report (`reports/report.html`).

---

## Project Structure

```text
config.py                  12-factor configuration with environment variable overrides
pages/
  ├── __init__.py          Package exports
  ├── base_page.py         BasePage with WebDriverWait, logging, and typed helpers
  ├── components/
  │     ├── __init__.py
  │     └── header_component.py Reusable universal Header & search bar component
  ├── home_page.py         eBay Home Page Object (composed with HeaderComponent)
  └── search_result_page.py eBay Search Results Page Object
tests/
  ├── conftest.py          WebDriver fixture, CLI options, hooks, failure attachments
  ├── test_title.py        Smoke tests for brand title and Motors navigation
  ├── test_search.py       Regression tests for single item search
  └── test_search_multiple.py Parametrized multi-item search regression suite
.github/workflows/
  └── qa.yml               CI/CD workflow: quality gate, test matrix, and report publishing
pyproject.toml             uv dependencies, pytest, ruff, pylint, and mypy settings
uv.lock                    Strict dependency lockfile
README.md                  Documentation and architecture overview
```
