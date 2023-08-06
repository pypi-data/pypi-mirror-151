# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](https://semver.org/).

## [0.0.3] - 2022-05-18
* Include flake8 linting of docstrings and style in Github Actions
* Include Windows tests in Github Actions
* Bug Fixes
  * Expanded cleaning of ICON IVM ion drifts to more variables
  * Fixed a bug in loading ICON IVM data (added multi_file_day = True)
  * Fixed a bug where OMNI meta data float values are loaded as arrays
* Maintenance
  * Removed dummy vars after importing instruments and constellations
  * Updated NEP29 compliance in Github Actions
  * Limit versions of hacking for improved pip compliance
  * Update instrument template standards
  * Updated documentation style
  * Removed cap on cdflib

## [0.0.2] - 2021-06-07
* Updated Instruments and routines to conform with changes made for pysat 3.0
* Added documentation
* Instrument Changes
  * Preliminary support added for SES-14 GOLD Nmax
  * Updated cleaning routines for C/NOFS IVM data
  * Migrated remote server for ICON instruments to SPDF from UCB
  * Renamed ROCSAT1 IVM as FORMOSAT1 IVM
  * Dropped support for SPORT IVM (unlaunched, moved to pysatIncubator)
* Implements GitHub Actions as primary CI test environment
* Improved PEP8 compliance
* Replaced pysatCDF with cdflib support
* Bug Fixes
  * `remote_file_list` error if start/stop dates unspecified
  * Improved download robustness

## [0.0.1] - 2020-08-13
* Initial port of existing routines from pysat
