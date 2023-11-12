# Digital Binder
Usage: Either run `python3 DigitalBinder.py` or run the executable `DigitalBinder.exe`.

This is a very barebones and shoddy implementation of a virtual binder for collectible cards. Known issues:
- The program may crash. I haven't found a consistent procedure for reproducing this issue unfortunately.
- The program leaks memory. Whenever a new binder or expansion is selected, the previous one does not get cleared.

As such I haven't published a release. Granted, I have no plans of further working on this project.

## Binders
Binders are stored as `<name>.<w>x<h>.txt` files. Where `<name>` is a custom name for the binder, otherwise not serving any function, `<w>` is the width or row-size (basically how many cards fit horizontally in a page of the binder) and `<h>` is the height or column-size (basically how many cards fit vertically in a page of the binder). `<w>` and `<h>` are assumed to each be a single digit in range \[0, 9\]. `<w>` can be, but does not need to be equal to `<h>`, however I've only tested 3x3 and 2x2 binders.

Each line in binder files corresponds to a relative path to an image file of the card that cardslot in the binder holds. If you want to create a new binder file with, say, room for 180 cards, you'll have to add 180 `Placeholder.png` lines to the file. [binderEmpty360.3x3.txt](binders/binderEmpty360.3x3.txt) serves as an example of a 3x3 empty binder with room for 360 cards.

You can flip pages in the binder by pressing the buttons at the bottom of the binder-frame. You can place a card in the binder by opening an expansion and drag'n'dropping the card to the binder slot. You can also swap two cards in the binder, by drag'n'dropping a card in the binder to a different slot. Finally, you can remove a card from the binder by right-clicking it. Use Ctrl-z to undo an action and Ctrl-Shift-z or Ctrl-y to redo an action.

You can scroll through the cards of an expansion by hovering over a displayed card and using the mousewheel. Alternatively, use the buttons to the right.

## Cards
Cards are expected to be .png files, size 245x342. They need to be organized by expansion. The [cards](cards) directory would contain subdirectories for each expansion. In these subdirectories, you'd put the cards. The [cards](cards) directory also contains `Placeholder.png` and `PlaceholderFilled.png` used for empty card slots in the binder.

DigitalBinder, by default, is setup for Pokémon TCG cards specifically. [ptcgExpansionDictionary.py](ptcgExpansionDictionary.py) is used to map and sort the expansion subdirectories in [cards](cards) to the names and release order of the expansion they represent. You can replace this dictionary and its `import` in [DigitalBinder.py](DigitalBinder.py) with a different one for different cards' expansions.

Whilst this repo doesn't come with any cards, they can be downloaded from elsewhere. You can run `python3 url/generateURL.py` to generate textfiles containing urls. If you have `wget` You can then run `wget -r -nv --no-parent -i <urlFileName>.txt -o out.txt` in a command prompt, replacing `<urlFileName>` with any of the previously generated `.txt` files to download pokémon card pngs from the (I believe) official website. Any `404 not found` errors for cards that couldn't be found can be found in the generated `out.txt` file. From what I can tell, this website doesn't have .pngs from cards that were released prior to the EX-era (~2003).

## Saving
During execution of DigitalBinder, by pressing the save button, a backup of the binder as it were after the last save is saved in [backups](binders/backups) with a timestamp in the name. Then, the original binder's file gets overwritten.