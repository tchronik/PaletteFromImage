#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2022 Terry Litrenta
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""
This extension will read the most used colours in an image and create an on-screen palette
using SVG rectangles that a user can then eye-drop on to set colours in their document.

"""

import inkex
import PIL.Image

# Following two functions are from simple_scripting.py, just slightly reduced.
def _python_to_svg_str(val):
    'Convert a Python value to a string suitable for use in an SVG attribute.'
    if isinstance(val, str):
        # Strings are used unmodified
        return val
    if isinstance(val, bool):
        # Booleans are converted to lowercase strings.
        return str(val).lower()
    if isinstance(val, float):
        # Floats are converted using a fair number of significant digits.
        return '%.10g' % val
    try:
        # Each element of a sequence (other than strings, which were
        # handled above) is converted recursively.
        return ' '.join([_python_to_svg_str(v) for v in val])
    except TypeError:
        pass  # Not a sequence
    return str(val)  # Everything else is converted to a string as usual.

def _construct_style(style):
        # Remove all keys whose value is None.
        style = {k: v for k, v in style.items() if v is not None}
        # Concatenate the style into a string.
        return ';'.join(['%s:%s' % kv for kv in style.items()])

def rgb2hex(rgb):
    return '#%02x%02x%02x' % rgb

def get_palette_colors(pil_img, palette_size=16, max_colours=5, ignore_white=True):
    # Reduce colors
    paletted = pil_img.convert('P', palette=PIL.Image.Palette.ADAPTIVE, colors=palette_size)

    # Find the color that occurs most often
    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)
    
    found_colors = 0
    colors = []

    # Loop through our colours and track up to our max_colours.
    for x in range(palette_size):
        if found_colors >= max_colours:
            break

        palette_index = color_counts[x][1]
        palette_color = palette[palette_index*3:palette_index*3+3]

        if (ignore_white and palette_color[0] == 255 and palette_color[1] == 255 and palette_color[2] == 255):
            continue
        else:
            found_colors+=1
            colors.append(tuple(palette_color))

    return colors

class PaletteGeneratorExtension(inkex.GenerateExtension):

    container_label = 'Palette'
    container_layer = True

    def add_arguments(self, pars):
        'Process program parameters passed in from the UI.'

        pars.add_argument('--swatchSize', type=int,
                          help='Size of swatches.')
        
        pars.add_argument('--swatchSpacing', type=int,
                        help='Spacing between each swatch.')

        pars.add_argument('--textColor', type=inkex.Color,
                        default=inkex.Color("black"),
                        help='Color used for the text.')       

        pars.add_argument('--imagePath', type=str,
                        help='Path to the palette image.')

        pars.add_argument('--showHexCode', type=inkex.Boolean,
                        help='Whether we want to show the hex code as text.')

        pars.add_argument('--ignoreWhiteInPalette', type=inkex.Boolean,
                        help='Ignore white (0xFFFFFF) in palette image.')

        pars.add_argument('--numPaletteSwatches', type=int,
                        help='Number of colour swatches in the palette image.')

        pars.add_argument("--orientation",
                        default="Top",
                        help="Orientation for the color swatches.")

    def create_palette_from_selection(self, num_palette_swatches, colours):
        sel = self.svg.selected
        bbox = sel.bounding_box()
        selSize = bbox.max - bbox.min

        box_width = selSize.x / num_palette_swatches
        box_height = selSize.y

        for index in num_palette_swatches.range():
            col = colours[index]
            colHex = rgb2hex(col)

            colStyle = {'fill' : colHex}
            
            x_pos = bbox.min.x + (index * box_width)
            y_pos = bbox.min.x

            self.rect((x_pos, y_pos), (box_width, box_height), round=0, style=colStyle)

    def generate(self):
        swatch_size = self.options.swatchSize
        swatch_spacing = self.options.swatchSpacing
        image_filename = self.options.imagePath
        show_hex_code = self.options.showHexCode
        ignore_white_in_palette = self.options.ignoreWhiteInPalette
        num_palette_swatches = self.options.numPaletteSwatches
        orientation = self.options.orientation
        text_color = self.options.textColor

        # Add just a bit of flare!
        radius = 2

        colors = []
        objects = []

        with PIL.Image.open(image_filename) as im:
            colors = get_palette_colors(im, max_colours=num_palette_swatches, ignore_white=ignore_white_in_palette)

        page_width = self.svg.viewbox_width
        page_height = self.svg.viewbox_height

        self.create_palette_from_selection(num_palette_swatches, colors)
        return

        index = 0

        for col in colors:
            colHex = rgb2hex(col)
            colStyle = {'fill' : colHex}

            x_pos = 0
            y_pos = 0

            # Sort out our x/y positions based on the orientation selected.
            if (orientation == "Top"):
                x_pos = (index * swatch_size) + (swatch_spacing * index)
                y_pos = -(swatch_size) - swatch_spacing
            elif (orientation == "Bottom"):
                x_pos = (index * swatch_size) + (swatch_spacing * index)
                y_pos = page_height + swatch_spacing
            elif (orientation == "Left"):
                x_pos = -(swatch_spacing) + -(swatch_size)
                y_pos = (index * swatch_size) + (swatch_spacing * index)
            elif (orientation == "Right"):
                x_pos = page_width + swatch_spacing
                y_pos = (index * swatch_size) + (swatch_spacing * index)

            # Create our swatch.
            objects.append(self.rect((x_pos, y_pos), (swatch_size, swatch_size), round=radius, style=colStyle))

            # Optionally, include the hex code on the swatch.
            if show_hex_code is True:
                color = text_color.to_rgb()
                new_col = (color[0], color[1], color[2])

                font_style = {'fill': rgb2hex(new_col),
                            'font-style' : 'normal',
                            'font-weight' : 'normal',
                            'font-size' : '5px',
                            'font-family' : 'sans-serif',
                            'text-align': 'center',
                            'vertical-align': 'top',
                            'text-anchor': 'middle'}

                text_x_pos = x_pos + (swatch_size / 2)
                text_y_pos = y_pos

                objects.append(self.text(colHex, (text_x_pos, text_y_pos), style=font_style))
            
            index+=1

        for o in objects:
            yield o

    def text(self, msg, location=None, style=None):
        text = inkex.TextElement()
        tspan = inkex.Tspan()
        tspan.text = msg
        
        ext_style = _construct_style(style)
        if ext_style != '':
            text.style = ext_style
        
        if location is not None:
            text.set('x', _python_to_svg_str(location[0]))
            text.set('y', _python_to_svg_str(location[1]))

        text.add(tspan)

        return text

    def rect(self, location, dimensions, round=None, style=None):
        _x = location[0]
        _y = location[1]

        _width = dimensions[0]
        _height = dimensions[1]

        # Create the rectangle
        obj = inkex.Rectangle(x = _python_to_svg_str(_x),
                            y = _python_to_svg_str(_y),
                            width = _python_to_svg_str(_width),
                            height = _python_to_svg_str(_height))

        # Set rounded edges on the rectangle
        try:
            rx, ry = round
        except TypeError:
            rx, ry = round, round

        if round is not None:
            obj.set('rx', _python_to_svg_str(rx))
            obj.set('ry', _python_to_svg_str(ry))

        ext_style = _construct_style(style)
        if ext_style != '':
            obj.style = ext_style

        return obj

if __name__ == '__main__':
    PaletteGeneratorExtension().run()
