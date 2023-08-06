pylypenko_first_package

### Build
```bash
python setup.py sdist bdist_wheel
```

### Check
```bash
twine check dist/*
```

### Send to test.pypi
```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

### Send to pypi
```bash
twine upload dist/*
```
