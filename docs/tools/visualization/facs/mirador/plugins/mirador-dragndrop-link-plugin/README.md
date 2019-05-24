# Mirador Drag and Drop Link Plugin

A Mirador plugin that adds the [IIIF drag and drop link](http://zimeon.github.io/iiif-dragndrop/) (manifest with canvas) to every window. This plugin will help you to open the current canvas in another IIIF viewer according to your purpose.

<a href="https://gist.githubusercontent.com/2SC1815J/4e4f2dd1d02b593e41e42fe4dd4c8293/raw/screenshot.png"><img src="https://gist.githubusercontent.com/2SC1815J/4e4f2dd1d02b593e41e42fe4dd4c8293/raw/screenshot_button.png"></a>

## Demo

- Mirador with Drag and Drop Link Plugin
    - [mirador-loader](http://2sc1815j.net/mirador-loader/?manifest=http://lab.ndl.go.jp/dhii/iiif/2537568/manifest.json&canvas=http://lab.ndl.go.jp/dhii/iiif/2537568/p16)

Implementation examples that support for a drop of “IIIF drag and drop” link (manifest with canvas):
- Mirador
    - http://2sc1815j.net/mirador-loader/
- Universal Viewer
    - http://2sc1815j.net/uv-loader/
- IIIF Curation Viewer
    - http://codh.rois.ac.jp/software/iiif-curation-viewer/demo/

## Usage

To enable it, include the CSS and the JavaScript (**after** loading Mirador).

```html
<link rel="stylesheet" type="text/css" href="<url to the plugin>/dragndrop-link.css" />
...
<script src="<url to the plugin>/dragndrop-link.js"></script>
```

## Acknowledgements

The most of this plugin (source code, description, etc.) is owed to “ManifestButton” a part of “[dbmdz] / [mirador-plugins]” (MIT License, Digital Library/Munich Digitization Center at Bavarian State Library). I would like to thank [dbmdz] for their activities.

[dbmdz]:https://github.com/dbmdz
[mirador-plugins]:https://github.com/dbmdz/mirador-plugins