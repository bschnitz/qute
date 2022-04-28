// ==UserScript==
// @name    Userstyle (qute.help.css)
// @include    qute://help*
// ==/UserScript==
GM_addStyle(`html {
  background-color: #041E39;
}

html > body, html ul > li > * {
  color: #EBEBD3;
  font-family: sans-serif;
}

html a {
  color: #F78764;
}

html a:visited {
  color: #2D8CF0;
}

.monospaced, code, pre {
  color: #F4D35E;
}

div.admonitionblock {
  color: #FAB49E;
  font-weight: bold;
}

html em, html dt {
  color: #FAB49E;
  font-weight: bold;
}

html div.listingblock > div.content, div.listingblock .highlight {
  background-color: #611B05;
}
`)