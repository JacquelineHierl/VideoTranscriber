# Video Transcriber
# Transcribe single or batch MP4 files into a text file
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from Transcriber import Transcriber


class GUIVideoTranscriber:
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("Video Transcriber")
        self.master.geometry("400x350")
        self.in_file = ""
        self.out_path = ""
        self.create_widgets()
        self.master.mainloop()

    def create_widgets(self):
        self.select_file_folder_label = tk.Label(self.master,
                                                 text="Select your input MP4 file(s), only German language supported")
        self.select_file_folder_label.pack(pady=5)

        self.select_file_button = tk.Button(self.master, text="Video File(s)", command=self.open_file_dialog,
                                            padx=20)
        self.select_file_button.pack(pady=5, padx=20)

        self.select_out_folder_label = tk.Label(self.master,
                                                 text="Output: Select target folder for textfile")
        self.select_out_folder_label.pack(pady=5)

        self.select_out_folder_button = tk.Button(self.master, text="Target Folder", command=self.open_out_folder_dialog)
        self.select_out_folder_button.pack(pady=5)

        self.path_label = tk.Label(self.master, text=f"No input file(s) selected {self.in_file}")
        self.path_label.pack(pady=5)

        self.out_path_label = tk.Label(self.master, text=f"No output folder selected {self.out_path }")
        self.out_path_label.pack(pady=5)

        self.start_transcript_button = tk.Button(self.master, text="Start Transcription", command=self.start_transcription)
        self.start_transcript_button.pack(side="bottom", pady=30)


    def open_file_dialog(self):
        list_of_paths = filedialog.askopenfilenames(initialdir="/", title="Select Video File",
                                              filetypes=(("Video files", "*.mp4"), ("all files", "*.*")))
        self.in_file = list_of_paths
        self.list_of_files = []
        #get list of filenames of path
        for file_path in list_of_paths:
            file_name = os.path.basename(file_path)
            self.list_of_files.append(file_name)

        self.path_label.pack_forget()
        self.path_label = tk.Label(self.master, text=f"Selected file(s): {self.list_of_files}")
        self.path_label.pack(pady=5)

    def open_out_folder_dialog(self):
        foldername = filedialog.askdirectory(initialdir="/", title="Select Targetfolder")
        self.out_path = foldername
        self.out_path_label.pack_forget()
        self.out_path_label = tk.Label(self.master, text=f"Selected Targetfolder: {self.out_path }")
        self.out_path_label.pack(pady=5)

    def start_transcription(self):
        if self.in_file == "" or self.out_path == "":
            messagebox.showerror("Paths not selected", "Please select output and input!")
            return
        else:
            messagebox.showinfo("Transcription in progress", message="Transcription in progress, excecution can take some minutes")
            Transcriber(self.in_file, self.out_path)
            messagebox.showinfo("Transcription successful", message="Transcription successful")


if __name__ == '__main__':
    GUIVideoTranscriber()
