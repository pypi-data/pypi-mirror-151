# Hartmann Wavefront software (HWS)

The HWS is software designed to process and operate the Hartmann Wavefront Sensing system at the LIGO and Virgo detectors.

As of 19th May 2022 (v2.1.0) the HWS source code was made open source by Peter Veitch.

Please direct packaging questions to daniel.d.brown@adelaide.edu.au.

# Fixing HWS

Changes should be submitted via merge requests. Merge requests should pass all tests and
requires approval. Version number must be bumped up manually. Each time a new a Wheel package
version is needed the version number must be bumped manually in `setup.py`.

# Releasing new version to Pypi

General advice can be found for releasing a package here: https://packaging.python.org/en/latest/tutorials/packaging-projects

```
rm -rf dist/hws-* # delete all existing distributions that have been built
python -m build
python -m twine upload dist/*
```
This will require access to a pypi account hosting the project.