# EFGM Validation Log

## 2026-05-21 - Initial Local Validation

Environment:

- Windows PowerShell
- Python 3.13.1
- pytest 9.0.3
- Repository path: `C:\_LOCALdata\SYSTEM\efgm`

Commands executed:

```bash
python -m pip install -e .
python -m pip install pytest
python -m pytest
efgm-score examples/weather_forecast_demo/input.json