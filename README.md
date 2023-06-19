# :steam_locomotive: Content-Train :steam_locomotive:

**This is an internal tool, there isn't any use outside our organization.**


## Short instructions for distribution staff

### Stop execution

1. Focus terminal window
2. Press `<Ctrl>+c`
3. Execution stops


### Resume copying files from distribution server

1. Focus terminal window
2. Type `python train import-files` or just use `<Arrow-Up>` until the command is visible.
3. Press `<Enter>`. The script will continuing it's work where it was stopped the last time.

(As this is a hacky script there is nothing which displays the state of copying a file, just be patience.)


### Resume transcoding

**Not implemented yet.**

1. Focus terminal window
2. Type `python train transcode` or just use `<Arrow-Up>` until the command is visible.
3. Press `<Enter>`. The script will continuing it's work where it was stopped the last time.
