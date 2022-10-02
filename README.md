# PaletteFromImage

Simple colour palette from image extension for Inkscape.

------------------------------------------------------------------------------------------------------------------------------
Disclaimer: I only started using Inkscape in the past few months and my Python sucks so I'll be happy to have input.

This was created with the sole purpose of being able to create an on-screen palette using SVG rectangles set to the colours from an image. I found myself using https://color.adobe.com/ colour palettes in a lot of my projects which meant downloading the palette image directly from the site and then pulling the jpeg file into the scene. This puts more overhead on Inkscape having a rasterized image in the document. This extension will look at the most used colours in an image (up to a maximum) and create SVG rectangles in the document representing these colours. Optionally, you can also choose to include the hex code for the colours. This makes selecting objects and then dropping directly on the palette very simple.

------------------------------------------------------------------------------------------------------------------------------

Instructions
------------

Save these files on your PC under this path:

C:\Users\<your username>\AppData\Roaming\inkscape\extensions

In Inkscape, under extensions, go to Image -> Palette From Image...

Screenshot
------------

![alt text](https://github.com/tchronik/PaletteFromImage/blob/main/PaletteFromImage.PNG?raw=true)