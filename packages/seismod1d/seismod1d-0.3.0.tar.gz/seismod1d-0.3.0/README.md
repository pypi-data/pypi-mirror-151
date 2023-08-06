# seismod1d
Synthetic seismic modelling of 1D elastic models.

## Getting started
```
virtualenv .venv
. ./.venv/Scripts/activate
pip install -r requirements.txt
pytest
```

## Release
Build and release new version to PyPI by:
```
git tag vX.X.X
git push --tags origin
```
