# -*- coding: utf-8 -*-

import sys

# START: Frawned approach to change default encoding
# But I intentionally take this approach since it's easy and believe it non-problematic in this limited program.
# See discussion detail here.
# https://stackoverflow.com/questions/3828723/why-should-we-not-use-sys-setdefaultencodingutf-8-in-a-py-script
reload(sys)
sys.setdefaultencoding('UTF8')
# END: Frawned approach to change default encoding

import StringIO
import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import time
import errno
from optparse import OptionParser
import re
import hashlib

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def get_filename(text):
    if re.search('[^\w\.\-_]', text):
        return hashlib.sha256(text.encode('utf-8')).hexdigest()
    else:
        return text

def save_snapshot(driver, word, idx):
    # fname = os.path.join(Options.dir, "%s.png" % get_filename(Options.prefix + word))
    fname = os.path.join(Options.dir, "%s.jpg" % get_filename(Options.prefix + word))
    idx = "%03d" % (idx + 1)

    if os.path.isfile(fname) and (not Options.force_save):
        print("  ! %s: %s exists!" % (idx, fname))
        return

    time.sleep(1)

    url_template = Engines[Options.engine]
    driver.get(url_template % word)

    if Options.js_before_save:
        with open(Options.js_before_save) as f:
            driver.execute_script(f.read())

    driver.execute_script("document.body.style.overflow = 'hidden';")

    # driver.save_screenshot(fname)
    screen = driver.get_screenshot_as_png()
    image = Image.open(StringIO.StringIO(screen))
    image.convert("RGB").save(fname, 'JPEG', optimize=True)
    print("  %s %s: %s" % (u'\u2713', idx, fname))

# https://gist.github.com/jsok/9502024
def optimize(driver):
    screen = driver.get_screenshot_as_png()
    (screen_width, screen_height) = Options.window.split("x")

    # Crop it back to the window size (it may be taller)
    image = Image.open(StringIO.StringIO(screen))
    box = (0, 0, screen_width, screen_height)
    region = image.crop(box)
    region.save('screen_lores.jpg', 'JPEG', optimize=True, quality=95)

def get_words_from_file(fname):
    with open(fname) as f:
        content = f.readlines()
    content = [x.split("\t")[0].rstrip() for x in content]
    return content

def retrieve_snapshot_for_words(driver, words):
    for idx, word in enumerate(words):
        save_snapshot(driver, word, idx)

Options = {}
Engines = {
    "google": 'https://www.google.com/search?gl=us&hl=en&pws=0&gws_rd=cr&tbm=isch&safe=active&q=%s',
    "google_unsafe": 'https://www.google.com/search?gl=us&hl=en&pws=0&gws_rd=cr&tbm=isch&q=%s',
    "bing": 'https://www.bing.com/images/search?safeSearch=Moderate&mkt=en-US&q=%s',
    "bing_unsafe": 'https://www.bing.com/images/search?safeSearch=Off&mkt=en-US&q=%s',
}

def main():
    global Options

    usage = "usage: %prog [options] word-list"
    scroll_to_first_image_of_google = "document.getElementById('islmp').scrollIntoView(true)"
    scroll_to_first_carousel_of_google = "document.getElementsByTagName('scrolling-carousel')[0].scrollIntoView()"

    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--dir", dest="dir", help="Directory to write captured images.", default="slideshow/imgs")
    parser.add_option("-j", "--js-before-save", dest="js_before_save", help="Eval js file before save mainly to scroll to element", default="")
    parser.add_option("-f", "--force-save", action="store_true", dest="force_save", help="Overwrite existing file if exists", default=False)
    parser.add_option("-p", "--prefix", dest="prefix", help="Prefix for filename", default="")
    parser.add_option("-w", "--window", dest="window", help="Window size. 1280x720 by default.", default="1280x720")
    parser.add_option("-e", "--engine", dest="engine", help="Image search engine to use one of %s" % Engines.keys(), default="google")
    parser.add_option("-s", "--show", action="store_true", dest="show", help="Do not hide chrome browser", default=False)
    (Options, args) = parser.parse_args()

    if Options.engine not in Engines:
        print("Engine must be one of %s" % Engines.keys())
        exit(1)

    chrome_options = webdriver.ChromeOptions()
    if not Options.show:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--hide-scrollbars')
    driver = webdriver.Chrome(options=chrome_options)

    (screen_width, screen_height) = Options.window.split("x")
    driver.set_window_size(screen_width, screen_height)
    print(Options)

    mkdir_p(Options.dir)

    for file in args:
        print(file + ': start')
        retrieve_snapshot_for_words(driver, get_words_from_file(file))
    driver.quit()

main()
