# PaletteFromImage

Simple colour palette from image extension for Inkscape.

------------------------------------------------------------------------------------------------------------------------------

This was created with the sole purpose of being able to create an on-screen palette using SVG rectangles set to the colours from an image. I found myself using https://color.adobe.com/ colour palettes in a lot of my projects which meant downloading the palette image directly from the site and then pulling the jpeg file into the document. This puts more overhead on Inkscape having a rasterized image in the document. This extension will look at the most used colours in an image (up to a maximum) and create SVG rectangles in the document representing these colours. Optionally, you can also choose to include the hex code for the colours. This makes selecting objects and then dropping directly on the palette very simple.

------------------------------------------------------------------------------------------------------------------------------

Instructions
------------

Save these files on your PC under this path:

C:\Users\<your username>\AppData\Roaming\inkscape\extensions

Then in Inkscape, under extensions, go to Image -> Palette From Image...

Options
------------

![alt text](https://github.com/tchronik/PaletteFromImage/blob/main/PaletteFromImage_Options.PNG?raw=true)

## Swatch Options

**Swatch Size** - Size of the swatch rectangle you want on-screen.

**Swatch Spacing** - How much spacing do you want between the swatches.

**Num Swatches In Palette** - How many total colours you want in your final palette.

**Show Hex Code & Text Colour** - Choose wether the hex code text sits above the swatches.

## Palette Options

**Use Selection For Palette** - Choose whether you want to use the active selections bounding box to generate a template for the palette. This will ignore swatch sizing and spacing in the swatch options.

**Ignore White From Palette** - Choose whether you want to ignore the colour white in the image. Certain images are saved with swatches on a stark white background. This might be undesirable when generating the palette as this colour would be considered "widely used".

**Palette Orientation** - Choose which side of the active page you want the palette to be created.

**Image Path** - Path to the image you want to load. This will be the image sampled to generate the palette based on the most used colours in the image.

Screenshot
------------

![alt text](https://github.com/tchronik/PaletteFromImage/blob/main/PaletteFromImage.PNG?raw=true)

You are also able to create a palette using an existing inkscape object as a template for your palette. In the screenshot below, this is a simple rectangle stretched across that then gets filled in with a palette. I tested this with a circle as well and it works, but the layout of the palette doesn't conform to the curves.

![alt text](https://github.com/tchronik/PaletteFromImage/blob/main/PaletteFromImage_Selection.PNG?raw=true)
