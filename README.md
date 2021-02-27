# database-rds-password-maintenance

connect to configured databases and reset the oracle password for given username

## Helpful Links

[tcl-tk install into pyenv](https://stackoverflow.com/questions/60469202/unable-to-install-tkinter-with-pyenv-pythons-on-macos)
[tcl-tk install into pyenv comment](https://github.com/pyenv/pyenv/issues/1375#issuecomment-533182043)

## initial python setup

### install pyenv/tcl-tk if needed
```
brew install pyenv
brew info tck-tk
brew install tcl-tk
```

### install python in pyenv with tcl-tk
Note I was getting an error after mig sur upgrade and had to do this:

`sudo xcode-select --switch /Applications/Xcode.app/`

```
pyenv uninstall 3.9.0
env \
  PATH="$(brew --prefix tcl-tk)/bin:$PATH" \
  LDFLAGS="-L$(brew --prefix tcl-tk)/lib" \
  CPPFLAGS="-I$(brew --prefix tcl-tk)/include" \
  PKG_CONFIG_PATH="$(brew --prefix tcl-tk)/lib/pkgconfig" \
  CFLAGS="-I$(brew --prefix tcl-tk)/include" \
  PYTHON_CONFIGURE_OPTS="--with-tcltk-includes='-I$(brew --prefix tcl-tk)/include' --with-tcltk-libs='-L$(brew --prefix tcl-tk)/lib -ltcl8.6 -ltk8.6'" \
  pyenv install 3.9.0
```

```
python3 -m pip install --user --upgrade pip
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```


## PySimpleGUI

[tutorial](https://realpython.com/pysimplegui-python/)
[examples](https://pypi.org/project/PySimpleGUI/#:~:text=PySimpleGUI%20is%20a%20Python%20package,%22Elements%22%20in%20PySimpleGUI)
[more examples](https://pysimplegui.trinket.io/demo-programs#/demo-programs/multi-threaded-work)