#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/6/27 20:10
# @Author  : 5in

import os
import win32com.client


# Two lines below generated from the command:
# python makepy.py -i VISLIB.DLLfrom win32com.client import gencache
# gencache.EnsureModule('{00021A98-0000-0000-C000-000000000046}', 0, 4, 11)

from win32com.client import constants

appVisio = win32com.client.Dispatch("Visio.Application")
appVisio.Visible =1

doc = appVisio.Documents.Add("Basic Diagram.vst")
pagObj = doc.Pages.Item(1)
stnObj = appVisio.Documents("Basic Shapes.vss")
mastObj = stnObj.Masters("Rectangle")

shpObj1 = pagObj.Drop(mastObj, 4.25, 5.5)
shpObj1.Text = "This is some text."

shpObj2 = pagObj.Drop(mastObj, 2, 2)
shpObj2.Text = "This is some more text."

connectorMaster = appVisio.Application.ConnectorToolDataObject

connector = pagObj.Drop(connectorMaster, 0, 0)
connector.Cells("BeginX").GlueTo(shpObj1.Cells("PinX"))
connector.Cells("EndX").GlueTo(shpObj2.Cells("PinX"))

doc.SaveAs(r'MyDrawing.vsd')
doc.Close()

appVisio.Visible =0
appVisio.Quit()