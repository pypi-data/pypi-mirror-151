# -*- coding: utf-8 -*-
# @Author: ander
# @Date:   2021-04-14 16:14:21
# @Last Modified by:   Anderson
# @Last Modified time: 2022-05-19 00:53:36
import os
import comtypes.client
from pathlib import Path


class PPTXConvertor:

    # https://docs.microsoft.com/en-us/office/vba/api/powerpoint.ppsaveasfiletype
    filetype_map = {
        'AnimatedGIF': 40,
        'BMP': 19,
        'Default': 11,
        'EMF': 23,
        'GIF': 16,
        'JPG': 17,
        'MP4': 39,
        'OpenDocumentPresentation': 35,
        'OpenXMLAddin': 30,
        'OpenXMLPicturePresentation': 36,
        'OpenXMLPresentation': 24,
        'OpenXMLPresentationMacroEnabled': 25,
        'OpenXMLShow': 28,
        'OpenXMLShowMacroEnabled': 29,
        'OpenXMLTemplate': 26,
        'OpenXMLTemplateMacroEnabled': 27,
        'OpenXMLTheme': 31,
        'PDF': 32,
        'PNG': 18,
        'Presentation': 1,
        'RTF': 6,
        'StrictOpenXMLPresentation': 38,
        'Template': 5,
        'TIF': 21,
        'WMV': 37,
        'XMLPresentation': 34,
        'XPS': 33,
    }

    fileext_map = {
        'AddIn': '.AddIn',
        'AnimatedGIF': '.gif',
        'BMP': '.bmp',
        'Default': '.pptx',
        'EMF': '.emf',
        'GIF': '.gif',
        'JPG': '.jpg',
        'MP4': '.mp4',
        'OpenDocumentPresentation': '.odp',
        'OpenXMLAddin': '.xml',
        'OpenXMLPicturePresentation': '.xml',
        'OpenXMLPresentation': '.xml',
        'OpenXMLPresentationMacroEnabled': '.xml',
        'OpenXMLShow': '.xml',
        'OpenXMLShowMacroEnabled': '.xml',
        'OpenXMLTemplate': '.xml',
        'OpenXMLTemplateMacroEnabled': '.xml',
        'OpenXMLTheme': '.xml',
        'PDF': '.pdf',
        'PNG': '.png',
        'Presentation': '.pptx',
        'RTF': '.rtf',
        'StrictOpenXMLPresentation': '.xml',
        'Template': '.potx',
        'TIF': '.tif',
        'WMV': '.wmv',
        'XMLPresentation': '.xml',
        'XPS': '.xps',
    }

    def __init__(self, input_path, output_path=''):
        self.input = Path(input_path)
        self.output = Path(output_path)

    def _convert_single_file(self, input_path, output_path):
        deck = self.powerpoint.Presentations.Open(os.path.abspath(input_path))
        deck.SaveAs(os.path.abspath(output_path), self.output_type_num)
        deck.Close()

    def convert(self, output_type='PDF'):
        if output_type in self.filetype_map:
            self.output_type_num = self.filetype_map[output_type]
        else:
            raise ValueError("Wrong output type. Must be one of [AddIn, AnimatedGIF, BMP, Default, EMF, ExternalConverter, GIF, JPG, MetaFile, MP4, OpenDocumentPresentation, OpenXMLAddin, OpenXMLPicturePresentation, OpenXMLPresentation, OpenXMLPresentationMacroEnabled, OpenXMLShow, OpenXMLShowMacroEnabled, OpenXMLTemplate, OpenXMLTemplateMacroEnabled, OpenXMLTheme, PDF, PNG, Presentation, RTF, Show, StrictOpenXMLPresentation, Template, TIF, WMV, XMLPresentation, XPS]")

        self.powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
        self.powerpoint.Visible = 1

        if self.input.is_file():
            if self.output.is_file():
                self._convert_single_file(self.input, os.path.abspath(self.output))
            else:
                output_path = self.output / (self.input.stem + self.fileext_map[output_type])
                self._convert_single_file(self.input, os.path.abspath(output_path))
        elif self.input.is_dir():
            if self.output.is_file():
                raise ValueError("Input parameter is a folder while output parameter is a file.")
            else:
                for child in self.input.iterdir():
                    if child.suffix not in ['.pptx', '.ppt']:
                        continue
                    self._convert_single_file(child, self.output / (child.stem + self.fileext_map[output_type]))
        else:
            raise ValueError("Input file or folder does not exist.")

        self.powerpoint.Quit()
