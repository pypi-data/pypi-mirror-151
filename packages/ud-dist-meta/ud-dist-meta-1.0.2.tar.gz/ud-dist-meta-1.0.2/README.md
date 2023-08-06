# Distribution metadata
This package is meant to provide information scrappers on distributions / repositories installed in the running environment.
It provides a command line api and python sdk, i.e.:
#### Command line
To gather metadata information from a distribution (e.g. spam) installed in the same environment as ```dist_meta```:
```commandline
gen_distinfo_cmd spam path\to\local\folder\configurations.yaml
```
This instruction will generate a YAML configuration file at the given location

#### Python
The base content of the package can be directly leverage, either through a script interface:
```python
import dist_meta
dist_meta.gen_distinfo_py("spam", r"path\to\local\folder\configurations.yaml")
```
Or directly leveraging the core package:
```python
import dist_meta
info_spam = dist_meta.DistInfo.from_env("spam")
print(info_spam.entry_points)
print(info_spam.environment)
print(info_spam.libraries)
print(info_spam.requirements)
info_spam.to_yaml (r"path\to\local\folder\configurations.yaml")
```
