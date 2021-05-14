# Yaml file translator

A Python script to automatically translate yaml files using google translator, very useful especially for frameworks
that reliy on yaml to manage their translation process (for example symfony)

## Usage

``` text
usage: translate.py [-h] [-l LANG] -f FILE [-st] [-o OUTPUT]

A command line program to translate yaml files

optional arguments:
  -h, --help            show this help message and exit
  -l LANG, --lang LANG  The language in which the yaml file will be
                        translated, the values must be equals to country codes
                        for example:en for english, fr for french ...
  -f FILE, --file FILE  Add the path of the file to be translated (name of the
                        file if it's at the same path as the script)
  -st, --single-threading
                        translate all values in the main thread instead of
                        splitting the translation process across different
                        threads, this will drastically slow down the
                        translation but it's safer to use to avoid google
                        blocking requests from the scripts
  -o OUTPUT, --output OUTPUT
                        Specify the file name of the translated output file


```

## Example usage

This will translate file.yaml located at the directory of the script to the French language, and it will name the result
file to "translated_file" (you can specify or not the extension yaml, it will be added automatically in case it wasn't
detected) all dependencies will be installed automatically

```
python translate.py -f file.yaml -l fr -o translated_file

```


