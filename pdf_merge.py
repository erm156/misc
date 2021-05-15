from tkinter import *
from tkinter import filedialog as fd
from PyPDF2 import PdfFileMerger


class MergeGUI:

    def __init__(self):
        window.configure(background="#a1dbcd")
        window.title("PDF Merge")

        l1 = Label(window,text="File 1",fg="#383a39",bg="#a1dbcd")
        l1.pack()

        self.t1 = Text(window,height=1,width=50)
        self.t1.pack()

        browse1 = Button(window,text="Browse",command=self.open_file1,highlightbackground="#a1dbcd")
        browse1.pack(pady=(0, 10))

        l2 = Label(window,text="File 2",fg="#383a39",bg="#a1dbcd")
        l2.pack()

        self.t2 = Text(window,height=1,width=50)
        self.t2.pack()

        browse2 = Button(window,text="Browse",command=self.open_file2,highlightbackground="#a1dbcd")
        browse2.pack(pady=(0, 15))

        merge_btn = Button(window,text="Merge!",command=self.merge_files,highlightbackground="#a1dbcd")
        merge_btn.pack()

        clear_btn = Button(window,text="Clear",command=self.clear_fields,highlightbackground="#a1dbcd")
        clear_btn.pack()


    def open_file1(self):
        window.fileName = fd.askopenfilename(filetypes=(("PDF files", "*.pdf"),("All files","*.*")))
        self.t1.delete("1.0",END)
        self.t1.insert(END,window.fileName)


    def open_file2(self):
        window.fileName = fd.askopenfilename(filetypes=(("PDF files", "*.pdf"),("All files","*.*")))
        self.t2.delete("1.0",END)
        self.t2.insert(END,window.fileName)


    def merge_files(self):
        path = fd.askdirectory()
        pdf_files = [self.t1.get("1.0","end-1c"), self.t2.get("1.0","end-1c")]
        merger = PdfFileMerger()
        for files in pdf_files:
            merger.append(files)
        merger.write(path + "/merged.pdf")


    def clear_fields(self):
        self.t1.delete("1.0",END)
        self.t2.delete("1.0",END)


if __name__ == '__main__':
    window = Tk()
    MergeGUI()
    window.mainloop()
