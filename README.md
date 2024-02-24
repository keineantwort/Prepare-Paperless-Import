# Prepare Paperless-ngx Import
Python script to prepare a filestructure to be imported into paperless-ngx.

NO WARRANTY for any problems! Use with care!

## Configuration
You need to create a `yaml` file to configure the import.

| field        | description                                                                              | Example                        |
|--------------|------------------------------------------------------------------------------------------|--------------------------------|
| `root`       | the root directory where all import directories are located                              | `/Users/martin/tmp/IMPORT`     |
| `target`     | the paperless dropoff import directory                                                   | `/Users/martin/_drop`          |
| `includes`   | a list of filetypes to import                                                            | `- pdf`<br/>`-jpg`             |
| `imports`    | a list of directories to import with their import configuration                          |                                |
| `dir`        | the directory name to import, which is located in `root`                                 | `Bank`                         |
| `targetdir`  | the target for this import as subdirectory of `target`                                   | `Bank`                         |
| `excludes`   | list of directories which should not be imported, but are located in `dir`               | `- Kontoauszüge`<br/>`- Name2` |
| `flatten`    | list of directories where all files subdirectories from subdirectories should be removed |                                |
| `pullup`     | nearly the same as flatten, but the directory itself will be removed too                 |                                |


Example:
```
root: /Users/martin/tmp/
target: "/Users/martin/paperless ngx/_drop"
includes:
  - pdf
  - jpg
imports:
  -
    dir: IMPORT/Bank
    targetdir: Bank
    excludes:
      - Bank1
      - "other Bank"
    flatten:
      - Bank 3
    pullup:
      - Postfach
  -
    dir: Another Bank Folder
    targetdir: Bank
    excludes:
    flatten:
    pullup:
```

Source file tree
```
Users
  +- martin
    +- tmp
      +- IMPORT
        +- Bank
          +- Bank1
            +- Doc1.pdf
            +- Doc2.pdf
          +- Bank2
            +- Doc 3.pdf
            +- some Excel file.xlsx
          +- other Bank
            +- Doc 4.pdf
          +- Bank 3
            +- Doc 1.pdf
            +- somedir
              +- Doc 1.pdf
          +- Bank 4
            +- Postfach
              +- 2023
                +- Doc 1.pdf
              +- 2024
                +- Doc 2.pdf
            +- Doc 1.pdf
      +- Another Bank Folder
        +- Bank2
          +- Doc 10.pdf
```

Result:
```
Users
  +- martin
    +- tmp
      +- IMPORT
        +- Bank
          +- Bank2
            +- Doc 3.pdf
            +- Doc 10.pdf
          +- Bank 3
            +- Doc 1.pdf
            +- somedir - Doc 1.pdf
          +- Bank 4
            +- Doc 1.pdf
            +- Doc 2.pdf
            +- 2023 - Doc 1.pdf
```