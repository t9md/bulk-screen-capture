var element;

element = document.getElementsByTagName("scrolling-carousel")[0];
if (!element) {
  element = document.getElementById("islmp"); // very first image
}

if (element) {
  element.scrollIntoView(true);
}
