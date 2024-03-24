import customtkinter
import tkinter.filedialog as filedialog


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.filename = None
        self._update_filename_label()

        self.geometry("400x150")

        self.button = customtkinter.CTkButton(
            self, text="Datei auswählen", command=self._select_file
        )
        self.button.pack(padx=20, pady=20)

        self.file_label = customtkinter.CTkLabel(master=self, text="")
        self.file_label.pack()

    def _select_file(self):
        self.filename = filedialog.askopenfilename(
            title="Bitte eine Datei auswählen", filetypes=[("IFC", "*.ifc")]
        )
        self._update_filename_label()

    def _update_filename_label(self):
        if self.filename:
            if not hasattr(self, "file_label"):  # Create label if it doesn't exist
                self.file_label = customtkinter.CTkLabel(master=self, text="")
                self.file_label.pack()
            self.file_label.configure(text=f"Ausgewählte Datei: {self.filename}")
        else:
            if hasattr(self, "file_label"):  # Remove label if filename is cleared
                self.file_label.destroy()
                del self.file_label


app = App()
app.mainloop()
