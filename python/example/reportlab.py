#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' ... '

__author__ = 'Sola'

from reportlab.lib import colors
from reportlab.graphics.shapes import *
from reportlab.graphics import renderPDF
from reportlab.graphics.charts.lineplots import LinePlot

data = [
    (2007, 8, 113.2, 114.2, 112.2),
    (2007, 9, 112.8, 115.8, 109.8),
    (2007, 10, 111.0, 116.0, 106.0),
    (2007, 11, 109.8, 115.3, 102.8),
    (2007, 12, 107.3, 114.2, 99.3),
    (2008, 1, 105.2, 114.1, 96.2),
    (2008, 2, 104.1, 110.9, 94.1),
    (2008, 3, 99.9, 106.8, 88.9),
    (2008, 4, 94.8, 104.2, 82.8),
    (2008, 5, 91.2, 114.2, 78.2),
]

drawing = Drawing(400, 200)

pred = [row[2]-40 for row in data]
high = [row[3]-40 for row in data]
low = [row[4]-40 for row in data]
times = [200*((row[0]+row[1]/12.0)-2007)-100 for row in data]

lp = LinePlot()
lp.x = 50
lp.y = 50
lp.height = 125
lp.width = 300

lp.data = [list(zip(times, pred)), list(zip(times, high)), list(zip(times, low))]
lp.lines[0].strokeColor = colors.blue
lp.lines[1].strokeColor = colors.red
lp.lines[2].strokeColor = colors.green

drawing.add(lp)

drawing.add(String(250, 150, 'Sunspots', fontSize=14, fillColor=colors.red))

renderPDF.drawToFile(drawing, 'hello.pdf', 'A simple PDF file!')