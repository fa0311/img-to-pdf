
import img2pdf
import glob
import re
from functools import cmp_to_key

class img_to_pdf:

    def convert(self, input, output = "output.pdf", extension = ".png"):
        img = [i.replace("\\","/") for i in glob.glob(f"{input}/**/*{extension}", recursive=True)]
        if len(img) == 0:
            raise ValueError("該当する画像ファイルがみつかりませんでした")
        sorted_img = sorted([i.lstrip(input) for i in img], key=cmp_to_key(self.sort))
        with open(output, "wb") as f:
            f.write(img2pdf.convert([f"{input}/{i}".encode('utf-8') for i in sorted_img]))

    def sort(self, a, b):
        reg = r'[0-9０-９]+'
        list_a = [int(i) for i in re.findall(reg, a)]
        list_b = [int(i) for i in re.findall(reg, b)]
        list_a_len = len(list_a)
        list_b_len = len(list_b)
        for key in range(list_a_len):
            if list_a_len <= key:
                return -1
            if list_b_len <= key:
                return 1
            if list_a[key] > list_b[key]:
                return 1
            if list_a[key] < list_b[key]:
                return -1
        return 0