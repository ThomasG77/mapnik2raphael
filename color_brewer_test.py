#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from tabdelim import DictReader

def list_code_colorbrewer(iterable):
    reader = DictReader(iterable)

    colors = []
    for row in reader:
        color_name = row["ColorName"]

        if color_name:
            colors.append(color_name)
    limit = colors.index('Apache-Style Software License for ColorBrewer software and ColorBrewer Color Schemes')
    filteredcolors = list(set(colors[:limit:]))
    filteredcolors.sort()
    return filteredcolors
    #return colors[:limit:]

import colorbrewer

lines = colorbrewer.resource_string(colorbrewer.PKG_DATA, colorbrewer.RES_COLORBREWER).splitlines()

color_list = list_code_colorbrewer(lines)

