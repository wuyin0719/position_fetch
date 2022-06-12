import ctypes
import os
class OCR():

    def __init__(self, DLL_PATH, TESSDATA_PREFIX, lang):
        self.DLL_PATH = DLL_PATH
        self.TESSDATA_PREFIX = TESSDATA_PREFIX
        self.lang = lang
        self.ready = False
        if self.do_init():
            self.ready = True


    def do_init(self):
        self.tesseract = ctypes.cdll.LoadLibrary(self.DLL_PATH)
        self.tesseract.TessBaseAPICreate.restype = ctypes.c_uint64
        self.api = self.tesseract.TessBaseAPICreate()
        rc = self.tesseract.TessBaseAPIInit3(ctypes.c_uint64(self.api), self.TESSDATA_PREFIX, self.lang)
        if rc:
            self.tesseract.TessBaseAPIDelete(ctypes.c_uint64(self.api))
            print('Could not initialize tesseract.\n')
            return False
        return True

    def get_text(self, path):
        if not self.ready:
            return False
        self.tesseract.TessBaseAPIProcessPages(
            ctypes.c_uint64(self.api), path, None, 0, None)
        self.tesseract.TessBaseAPIGetUTF8Text.restype = ctypes.c_uint64
        text_out = self.tesseract.TessBaseAPIGetUTF8Text(ctypes.c_uint64(self.api))
        return bytes.decode(ctypes.string_at(text_out)).strip()



def orc_run():
    from PIL import Image, ImageGrab

    im = ImageGrab.grabclipboard()

    if isinstance(im, Image.Image):
        print("Image: size : %s, mode: %s" % (im.size, im.mode))
        im.save('test.png')
        # im.save("grab_grabclipboard.jpg")
    elif im:
        for filename in im:
            try:
                print("filename: %s" % filename)
                im = Image.open(filename)
            except IOError:
                pass  # ignore this file
            else:
                print("ImageList: size : %s, mode: %s" % (im.size, im.mode))
    else:
        print("clipboard is empty.")


    # DLL_PATH = r'E:\工作\【程序开发案例】\Python\文字识别\python_tesseract_dll\python_tesseract_dll\libtesseract304.dll'
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    DLL_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),'libtesseract304.dll')
    TESSDATA_PREFIX = os.path.join(os.path.dirname(os.path.realpath(__file__)),'tessdata')
    # print(TESSDATA_PREFIX)
    # print(DLL_PATH)
    TESSDATA_PREFIX = b'.//tessdata'
    lang = b'eng'
    ocr = OCR(DLL_PATH, TESSDATA_PREFIX, lang)
    image_file_path = b'test.png'
    result = ocr.get_text(image_file_path)
    print(result)

    return result
if __name__ == '__main__':
    orc_run()
    # DLL_PATH = 'libtesseract304.dll'
    # DLL_PATH = r'E:\工作\【程序开发案例】\Python\文字识别\python_tesseract_dll\python_tesseract_dll\libtesseract304.dll'
    # TESSDATA_PREFIX = b'./tessdata'
    # lang = b'eng'
    # ocr = OCR(DLL_PATH, TESSDATA_PREFIX, lang)
    # image_file_path = b'test.png'
    # result = ocr.get_text(image_file_path)
    # print(result)