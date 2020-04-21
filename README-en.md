<!-- TOC START min:1 max:3 link:true asterisk:true update:true -->
* [What's this?](#whats-this)
* [Environment](#environment)
* [Preparation](#preparation)
* [Let's start](#lets-start)
  * [Lets' read `help`](#lets-read-help)
  * [Lets'collect screenshot for words in file.](#letscollect-screenshot-for-words-in-file)
  * [Refer collected image from Anki Deck](#refer-collected-image-from-anki-deck)
    * [1. Put images to Anki's media folder](#1-put-images-to-ankis-media-folder)
    * [2. Add a reference to the image to new field of card](#2-add-a-reference-to-the-image-to-new-field-of-card)
<!-- TOC END -->

# What's this?

Bulk screen capture script intended to use for Anki.

- Read the list of words from a file then search the corresponding image via google-image to auto-capture screenshot.
- When you remember a new word by Anki, the image helps a lot to grasp the initial clue what that word means, but it is also super tedious to manually collect images and put it into each card. Also, choosing the most appropriate picture from the result of the image search is another headache when you are not familiar with the word. So the idea is to capture the whole screenshot which includes multiple images.
- This is NOT Anki add-on. This is a simple script to collect a screenshot of image-search. Then you can use this collected image to refer from each card in Anki which is also easily achievable by bulk modifying tsv file.

# Environment

- I confirmed this works with Python 2.7.16 which is the system default of my macOS.
- I believe you can use it in Windows with slight modification.
- I believe you can use it in Python 3.x with slight modification.

# Preparation

- Install [Chrome driver](http://chromedriver.chromium.org/downloads) ant put it in `PATH`(like `/usr/local/bin`). Type `chromedriver -h` in SHELL should show some output.
- Install `selenium` and `pillow`

```sh
$ pip install selenium pillow
```

# Let's start

## Lets' read `help`

Observe which options are available. `--show` options prevent a browser from hiding, which is especially useful when you tweak window size option.

```sh
$ python bulk-screen-capture.py -h
```

## Lets'collect screenshot for words in file.

- This script sleeps 1 second on each search. The reason for this is to prevent Google to see this script as BOT and ban access.
- So a thousand words roughly take over 20 min to finish. It is good idea to use utility soft such as  Amphetamine to keep macOS awake.

```python
python bulk-screen-capture.py -d collection.media -p "google-img--" -j before_scroll.js -w 720x720 sample.tsv
```

- `-d collection.media`: Specify a directory to store screenshots.
- `-p "google-img--"`: Prefix for file name. Anki media files need to reside directly on the media folder to be synced across devices. So I wanted generated files to be easily distinguishable.
- `-j before_scroll.js`: JavaScript file executed just before screenshot(used to tweak scroll position).
- `-w 720x720`: Window size. The larger size is good for quality but the file size becomes bigger.
- `sample.tsv`: Pass filename as the last arg. Use the very first field of TSV(Tab-separated values). You can put a single field file of course.

sample.tsv
```
tactic	戦術、戦法、作戦
backfire	計画などが裏目に出る、エンジン・車がさか火を起こす
catastrophic	壊滅的な、大異変の、最悪の
```

The images below are a screenshot of `tactic`, `backfire`, `catastrophic`.

<p>
<img style="border: 2px black solid;" src="./imgs/google-img--tactic.jpg" width="300">
<img style="border: 2px black solid;" src="./imgs/google-img--backfire.jpg" width="300">
<img style="border: 2px black solid;" src="./imgs/google-img--catastrophic.jpg" width="300">
</p>

What `before_scroll.js` does?

Tweaking scroll position to bring the best experience.

Take the following pic as an explanation.
- `A`: This section is useless, so it should be eliminated from screenshot. I want the scroll to `B` or `C` position.
- `B`: This section is quite beneficial to understand how this word is used.
- `C`: However not all word show `B` section, in that case, scroll to `C`.

<p>
<img src="./imgs/Google_Search.png" width="600">
</p>

## Refer collected image from Anki Deck

### 1. Put images to Anki's media folder

Put. Put it there.
For the size of disk space, I collected a total of 3000 files with a 720x720 window size, which resulted in the size of 572MB.

### 2. Add a reference to the image to new field of card

I put [add_img_field.rb](https://github.com/t9md/bulk-screen-capture/blob/master/add_img_field.rb) as sample. This script adds the image reference field to the last field by using the very first field as search word. Hope you can tweak this script to your own need.

Example use
```sh
$ cat sample.tsv
tactic  戦術、戦法、作戦
backfire        計画などが裏目に出る、エンジン・車がさか火を起こす
catastrophic    壊滅的な、大異変の、最悪の
$ ruby add_img_field.rb sample.tsv > sample-new.tsv
ma
