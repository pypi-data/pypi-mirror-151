# PPTXCONVERTOR
Simple pptx file convertor. Powerpoint application is required.

[中文文档](README-CN.md)

## Installation

```
pip install PPTXConvertor
```

## Example

```Python
from PPTXConvertor import PPTXConvertor

convertor = PPTXConvertor('path/to/input/folder_or_file')
convertor.convert('PDF')
convertor.convert('JPG')
```

```Python
from PPTXConvertor import PPTXConvertor

convertor = PPTXConvertor('path/to/input/folder_or_file', 'path/to/output/folder_or_file')
convertor.convert('PDF')
convertor.convert('JPG')
```

## Supported formats

According to [PpSaveAsFileType](https://docs.microsoft.com/en-us/office/vba/api/powerpoint.ppsaveasfiletype), the following types are supported.

So parameter in convert() function must be one of the following name string.

- AddIn
- AnimatedGIF
- BMP
- Default
- EMF
- ExternalConverter
- GIF
- JPG
- MetaFile
- MP4
- OpenDocumentPresentation
- OpenXMLAddin
- OpenXMLPicturePresentation
- OpenXMLPresentation
- OpenXMLPresentationMacroEnabled
- OpenXMLShow
- OpenXMLShowMacroEnabled
- OpenXMLTemplate
- OpenXMLTemplateMacroEnabled
- OpenXMLTheme
- PDF
- PNG
- Presentation
- RTF
- Show
- StrictOpenXMLPresentation
- Template
- TIF
- WMV
- XMLPresentation
- XPS