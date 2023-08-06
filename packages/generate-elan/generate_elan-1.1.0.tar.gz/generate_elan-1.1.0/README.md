# GENERATE ELAN

This package reads all the audio files in the directory and generates an ELAN file for each audio file.

## Installing

You can install this package by running the following command from PyPi:

```bash
pip install generate-elan
```

## How to use

Generate ELAN files (with `.eaf` extension) from of audio files from a directory:

```bash
python -m generate_elan -d DIRECTORY
```

You can also specify some options:

```bash
-d DIRECTORY, --directory DIRECTORY
                        Directory containing audio files
-e EXTENSION, --extension EXTENSION
                        Audio extension
```
