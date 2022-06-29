#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/6/22 16:05
# @Author  : 5in

from .imageShow_dialog import ImageShowDialog
import os
from qgis.core import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtCore import *
from qgis.utils import iface
# class imageShowmain():
#     def __init__(self):
#         self.dlg = ImageShowDialog()
#         self.dlg.show()
#
#     def run(self):
#         result = self.dlg.exec_()
#         # See if OK was pressed
#         if result:
#             print('xxxxx')


def imageShowmain():
    dlg = ImageShowDialog()
    layers = iface.mapCanvas().layers()
    dlg.comboBox.clear()
    dlg.comboBox.addItems([layer.name()for layer in layers])

    def changelayer():
        index = dlg.comboBox.currentIndex()
        layer = layers[index]
        # fields = layer.fields()
        # fieldnames = [field.name() for field in fields]
        try:
            fields = layer.fields()
            fieldnames = [field.name() for field in fields]
        except:
            fieldnames = []
        dlg.comboBox_2.clear()
        dlg.comboBox_2.addItems(fieldnames)

        # print(dlg.comboBox.currentIndex())
    # show the dialog
    changelayer()
    dlg.comboBox.currentIndexChanged.connect(changelayer)


    dlg.show()
    # Run the dialog event loop
    result = dlg.exec_()
    # See if OK was pressed
    if result:
        i = dlg.comboBox.currentIndex()
        attr_i = dlg.comboBox_2.currentIndex()

        # print('xxxxx')
        # print(i)
        enumerateBypolygon(attr_i)


def enumerateBypolygon(attr_i):
    import os
    desk = os.path.join(os.path.expanduser("~"), 'Desktop') + '\\' + 'QGIS_Result'
    os.makedirs(desk, exist_ok=True)
    # features = iface.activeLayer().getFeatures()
    for feature in iface.activeLayer().getFeatures():
        ext=feature.geometry().boundingBox()
        image_location=os.path.join(desk,'%s.png'%feature[attr_i])
        simpeRender(ext,image_location)
    # ext = next(features).geometry().boundingBox()


def simpeRender(ext,image_location):


    # image_location = os.path.join(QgsProject.instance().homePath(), "render.png")

    # vlayer = iface.activeLayer()
    settings = QgsMapSettings()
    # layers = [layer for layer in QgsProject.instance().mapLayers().values()]
    layers = iface.mapCanvas().layers()
    # settings.setLayers(layers)
    settings.setLayers(layers)
    # settings.setLayers([iface.activeLayer(),iface.activeLayer()])

    settings.setBackgroundColor(QColor(255, 255, 255))

    settings.setOutputSize(QSize(800, ext.height()*800/ext.width()))
    # settings.setOutputSize(QSize(800, 600))
    settings.setDestinationCrs(layers[0].crs())



    iface.mapCanvas().setExtent(ext);
    iface.mapCanvas().refresh();
    settings.setExtent(ext)

    # settings.setExtent(iface.activeLayer().extent())
    # print(iface.mapCanvas().extent().toString())
    render = QgsMapRendererParallelJob(settings)

    def finished():
        img = render.renderedImage()
        # save the image; e.g. img.save("/Users/myuser/render.png","png")
        img.save(image_location, "png")

    render.finished.connect(finished)

    # Start the rendering
    render.start()

    # The following loop is not normally required, we
    # are using it here because this is a standalone example.
    from qgis.PyQt.QtCore import QEventLoop
    loop = QEventLoop()
    render.finished.connect(loop.quit)
    loop.exec_()