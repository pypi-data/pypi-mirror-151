# pylint-json2checkstyle

A Pylint plugin and command line tool to produce Pylint reports in checkstyle format.

This project is partially inspired from the [pylint-json2html](https://github.com/Exirel/pylint-json2html) project.

## Usage:
### As a command line tool
```
usage: pylint-json2checkstyle [-h] [-o checkstyle_output_file] [json_input_file]

Convert pylint json report to checkstyle

positional arguments:
  json_input_file       Pylint JSON report input file (or stdin)

optional arguments:
  -h, --help            show this help message and exit
  -o checkstyle_output_file, --output checkstyle_output_file
                        Checkstyle report output file (or stdout)
```

### As a Pylint plugin:
```
pylint --load-plugins=pylint_json2checkstyle.checkstyle_reporter --output-format=checkstyle [pylint arguments ... ]
```

## Why?
Checkstyle is a widely supported report format for code issues, with integrations available in CI environments.

For example, the [Checkstyle GitHub Action](https://github.com/jwgmeligmeyling/checkstyle-github-action) reads a checkstyle report and adds
annotations to PRs.

