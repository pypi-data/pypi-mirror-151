# PatrowlManagerSDK
Python API Client for PatrowlArsenal

# Pypi Deployment commands
```
rm -rf dist/ build/ PatrowlManagerSDK.egg-info
python setup.py sdist bdist_wheel
twine upload dist/*
```

# Local setup for tests
pip install -e .
set env var in pytest.ini
pytest tests/test_{name}
pytest tests/*