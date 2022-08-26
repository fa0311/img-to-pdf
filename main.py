import asyncio
import tkinter
import tkinter.filedialog
import tkinter.scrolledtext
from lib.img_to_pdf import img_to_pdf
import webbrowser

APP_NAME = "img-to-pdf"
VERSION = "1.2.0"


class input_window:
    def __init__(self, debug=False):
        self.debug = debug
        self.window = tkinter.Tk()
        self.window.title("img-to-pdf")
        self.window.geometry("400x200")

    def run(self):
        tkinter.Label(self.window, text="フォルダ").grid(
            column=0,
            row=1,
            columnspan=1,
            pady=5,
            padx=0,
        )
        folder_dialog_button = tkinter.Button(self.window, text="選択", width=20)
        folder_dialog_button.bind("<ButtonPress>", self.folder_dialog)
        folder_dialog_button.grid(
            column=1,
            row=1,
            columnspan=1,
            pady=5,
            padx=0,
        )

        self.folder_name = tkinter.StringVar(self.window)
        tkinter.Label(self.window, textvariable=self.folder_name).grid(
            column=0,
            row=2,
            columnspan=2,
            pady=0,
            padx=0,
        )

        tkinter.Label(self.window, text="画像の拡張子").grid(
            column=0,
            row=3,
            columnspan=1,
            pady=0,
            padx=0,
        )
        self.extension = tkinter.StringVar(self.window)
        self.extension.set(".png")
        tkinter.Entry(self.window, textvariable=self.extension).grid(
            column=1,
            row=3,
            columnspan=2,
            pady=0,
            padx=0,
        )

        tkinter.Label(self.window, text="出力先ファイル").grid(
            column=0,
            row=4,
            columnspan=1,
            pady=0,
            padx=0,
        )
        self.output_path = tkinter.StringVar(self.window)
        self.output_path.set("output.pdf")
        tkinter.Entry(self.window, textvariable=self.output_path).grid(
            column=1,
            row=4,
            columnspan=2,
            pady=0,
            padx=0,
        )

        enter_button = tkinter.Button(self.window, text="実行", width=50)
        enter_button.bind("<ButtonPress>", self.click)
        enter_button.grid(
            column=0,
            row=5,
            columnspan=2,
            pady=5,
            padx=20,
        )

        enter_update = tkinter.Button(self.window, text="アップデートの確認", width=50)
        enter_update.bind("<ButtonPress>", self.update_dialog)
        enter_update.grid(
            column=0,
            row=6,
            columnspan=2,
            pady=5,
            padx=20,
        )

        tkinter.Label(
            self.window,
            text="{app_name} v{version}".format(app_name=APP_NAME, version=VERSION),
        ).grid(
            column=0,
            row=7,
            columnspan=2,
        )
        return self

    def folder_dialog(self, event=None):
        folder_name = tkinter.filedialog.askdirectory(initialdir=self.folder_name.get())
        if len(folder_name) > 0:
            self.folder_name.set(folder_name)

    def update_dialog(self, event=None):
        webbrowser.open("https://github.com/fa0311/img-to-pdf/releases")

    def click(self, event=None):
        if self.debug:
            self.to_pdf()
        else:
            asyncio.new_event_loop().run_in_executor(None, self.to_pdf)

    def to_pdf(self):
        progress = progress_window().run()
        try:
            if len(self.folder_name.get()) == 0:
                raise ValueError("フォルダが存在しないためエラーが発生しました")
            img_to_pdf().convert(
                self.folder_name.get().replace("\\", "/"),
                output=self.output_path.get(),
                extension=self.extension.get(),
            )
            progress.text.set("完了しました")
        except Exception as e:
            progress.text.set(e)


class progress_window:
    def __init__(self):
        self.window = tkinter.Toplevel()
        self.window.geometry("400x200")

    def run(self):
        self.text = tkinter.StringVar(self.window)
        self.text.set("実行中です")
        tkinter.Label(self.window, textvariable=self.text).pack()
        return self


if __name__ == "__main__":
    input_window(debug=False).run().window.mainloop()
