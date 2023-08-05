![coverage badge](./badges/coverage.svg) [![CI](https://github.com/cerebre-io/ceader/actions/workflows/CI.yaml/badge.svg)](https://github.com/cerebre-io/ceader/actions/workflows/CI.yaml) [![PyPI version](https://badge.fury.io/py/ceader.svg)](https://badge.fury.io/py/ceader)

<!-- ![Your Repository's Stats](https://github-readme-stats.vercel.app/api?username=JankowskiKamil&show_icons=true) -->
# Ceader

Tool for automatically adding a header to files in the form of a comment.\
Based on the file extensions, Ceader detects the programming language and selects the comment character accordingly.

Header sample, created by [this](https://patorjk.com/software/taag/#p=display&f=Graffiti&t=Type%20Something%20) software:


```
                    _                _
   ___ ___ _ __ ___| |__  _ __ ___  (_) ___
  / __/ _ \ '__/ _ \ '_ \| '__/ _ \ | |/ _ \
 | (_|  __/ | |  __/ |_) | | |  __/_| | (_) |
  \___\___|_|  \___|_.__/|_|  \___(_)_|\___/

Proprietary software created by CEREBRE.
© CEREBRE, USA. All rights reserved.
Visit us at: https://www.cerebre.io
```

Sample output:

.py file without header:
```
print("Hello world!")
```
.py file with header:
```
#                    _                _
#   ___ ___ _ __ ___| |__  _ __ ___  (_) ___
#  / __/ _ \ '__/ _ \ '_ \| '__/ _ \ | |/ _ \
# | (_|  __/ | |  __/ |_) | | |  __/_| | (_) |
#  \___\___|_|  \___|_.__/|_|  \___(_)_|\___/
#
#Proprietary software created by CEREBRE.
#© CEREBRE, USA. All rights reserved.
#Visit us at: https://www.cerebre.io
print("Hello world!")
```

If the header already exists, in the same form as in the given ```${HEADER_PATH}``` file, the header will not be added a second time.

### Installation
From [PyPi](https://pypi.org/project/ceader/)
```
pip install ceader
```
### Exemplary cli usage
```
ceader --mode add_header --files ${FILES} --header-path ${HEADER_PATH} --extensions ${EXTENSIONS}  --prefer-multiline-comment --debug --skip-hidden
```

### Pre-commit plugin
In order to use ceader in pre-commit, the following two configs are recommended:
- always run on the specified files.
- run at certain stages (by default repo ceader use ```stages: all stages```, check pre-commit [documentation](https://pre-commit.com/)).

##### Always run

Add the following configuration to your .pre-commit-config.yaml:
```
repos:
    - repo: https://github.com/cerebre-io/ceader
        rev: 0.0.6
        hooks:
        - id: ceader
            args:[
                '--mode', ${MODE},
                '--header-path', ${HEADER_PATH},
                '--extensions', ${EXTENSIONS},
                '--debug',
                '--skip-hidden',
                '--files', ${FILES}]
            pass_filenames: false
```

With this config ceader will try to change ```${FILES}``` every time.
##### Run at certain stages
Add the following configuration to your .pre-commit-config.yaml:
```
repos:
    - repo: https://github.com/cerebre-io/ceader
        rev: 0.0.6
        hooks:
        - id: ceader
            args:[
                '--mode', ${MODE},
                '--header-path', ${HEADER_PATH},
                '--extensions', ${EXTENSIONS},
                '--debug',
                '--skip-hidden',
                '--files']
            stages: "add stages here"
```
With this config ceader will try to change files provided by pre-commit on given stages.
```stages``` is optional, because by default stages: all stages
###### FILES
This is the List of Paths to folders or directly to files that need to be changed. In folders, files will be searched recursively.

###### HEADER_PATH
Path to the file in .txt format with the header to be added.

###### EXTENSIONS
Files with these extensions will be searched for in the ```${FILES}```. \
The programming language will be recognized by this information and an appropriate comment will be added.
Supported extensions and languages can be found [here](https://github.com/cerebre-io/ceader/blob/main/ceader/domain/knowledge/extensions_to_language.py).

###### DEBUG
An optional boolean value that allows checking the status of adding headers.
If you are using precommit, ```verbose: true``` must be provided in config.

###### PREFER_MULTILINE_COMMENT
Some languages ​​support block comments and also single comments and some of them only one type of comment.\
By default ceader will use try to use single comment if possible. If this is not possible it will use block comment. \
Use ```--prefer-multiline-comment``` if you want to reverse logic.

###### SKIP_HIDDEN
An optional boolean that allows you to ignore hidden files, even if they meet the extension condition.


###### MODE

There are two modes at the moment:\
    - ```add_header``` adds the indicated header to files, if header already exists in the file it does nothing.\
    - ```remove_header``` removes the indicated header to files, but only if header exists in the file.




### TODO

- user validation (e.g: lint)
- files backup - pre-commit provides backup but the app itself not
- change extensions arg to optional - if not used, change all files
