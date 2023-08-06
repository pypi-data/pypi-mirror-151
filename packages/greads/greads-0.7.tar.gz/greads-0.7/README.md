# Goodreads Quotes Scraper


## Requirements
- [python>=3.6](https://www.python.org/downloads/)

## Installation

```sh
pip install greads
```

## Usage

```sh
greads --help
```

```
usage: greads [-h] -a AUTHOR [-l LANGUAGE] [-n NUM_PAGES] [-o OUTPUT_FILE]
            [--enable-multiprocessing]

optional arguments:
  -h, --help            show this help message and exit
  -a AUTHOR, --author AUTHOR
                        Full name of the author you want to search
  -l LANGUAGE, --language LANGUAGE
                        Two letters string representing the language you want
                        to parse the results in (default: en)
  -n NUM_PAGES, --num-pages NUM_PAGES
                        Number of pages to iterate through (if empty, will
                        iterate through all pages)
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Name of the output file (default: quotes.json)
  --enable-multiprocessing
                        Enable multiprocessing
```


## Example


```sh
greads --author "Oscar Wilde" --num-pages 100
# 100%|█████████████████████████████████████████| 100/100 [01:06<00:00,  1.49it/s]
# Cleaning the quotes text...
# Saved results to quotes.json...
```

```sh
greads --author "Oscar Wilde" --num-pages 10 --language 'es'
# 100%|███████████████████████████████████████████| 10/10 [00:06<00:00,  1.60it/s]
# Cleaning the quotes text...
# Saved results to quotes.json...
```
