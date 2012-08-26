__author__ = 'Yaroslav Nikityshev aka IDNoise'

import os
import wx
import yaml
import shutil
from idn_global import GetMainFrame
from idn_utils import CreateButton

class Config:
    COLOR_SCHEMA = "color_schema"
    USER_NAME = "user_name"

    @classmethod
    def load(cls):
        firstTime = False
        path = os.path.join(GetMainFrame().cwd, "noiseide.yaml")
        if not os.path.isfile(path):
            shutil.copy2(os.path.join(GetMainFrame().cwd, "noiseide.template.yaml"), path)
            firstTime = True
        stream = file(path, 'r')
        cls.data = yaml.load(stream)
        if firstTime:
            form = ConfigEditForm()
            form.ShowModal()

    @classmethod
    def save(cls):
        path = os.path.join(GetMainFrame().cwd, "noiseide.yaml")
        stream = file(path, 'w')
        yaml.dump(cls.data, stream)

    @classmethod
    def GetProp(cls, prop):
        if prop in cls.data:
            return cls.data[prop]
        return None

    @classmethod
    def SetProp(cls, prop, value):
        cls.data[prop] = value
        cls.save()

    @classmethod
    def UserName(cls):
        return (cls.data[cls.USER_NAME] if cls.USER_NAME in cls.data else "NoiseIDE User")

    @classmethod
    def ColorSchema(cls):
        return (cls.data[cls.COLOR_SCHEMA] if cls.COLOR_SCHEMA in cls.data else "dark")


class ConfigEditForm(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, GetMainFrame(), size = (290, 120), title = "Edit config")

        sizer = wx.GridBagSizer(2, 2)
        self.colorSchemas = []
        for file in os.listdir(GetMainFrame().cwd):
            if file.endswith(".color.yaml"):
                self.colorSchemas.append(file.split(".")[0])
        self.colorSchemaCB = wx.ComboBox(self, choices = self.colorSchemas,
            value = Config.ColorSchema(),
            size = (180, 25),
            style = wx.CB_READONLY
        )
        self.userNameTB = wx.TextCtrl(self, value = Config.UserName(), size = (180, 25))
        self.closeButton = CreateButton(self, "Close", self.OnClose)
        self.saveButton = CreateButton(self, "Save", self.OnSave)

        sizer.Add(wx.StaticText(self, label = "Color schema:"), (0, 0), flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL, border = 2)
        sizer.Add(self.colorSchemaCB, (0, 1), flag = wx.ALL | wx.wx.ALIGN_LEFT, border = 2)
        sizer.Add(wx.StaticText(self, label = "User name:"), (1, 0), flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL, border = 2)
        sizer.Add(self.userNameTB, (1, 1), flag = wx.ALL | wx.wx.ALIGN_LEFT, border = 2)
        sizer.Add(self.closeButton, (2, 0), flag = wx.ALL | wx.wx.ALIGN_LEFT, border = 2)
        sizer.Add(self.saveButton, (2, 1), flag = wx.ALL | wx.wx.ALIGN_RIGHT, border = 2)

        self.SetSizer(sizer)
        self.Layout()

    def OnClose(self, event):
        self.Close()

    def OnSave(self, event):
        if self.colorSchemaCB.Value in self.colorSchemas:
            Config.SetProp(Config.COLOR_SCHEMA, self.colorSchemaCB.Value)
        if self.userNameTB.Value:
            Config.SetProp(Config.USER_NAME, self.userNameTB.Value)
        self.Close()