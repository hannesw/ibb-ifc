import customtkinter
import tkinter.filedialog as filedialog
import lib.bbsoft as bbsoft
import lib.model_checker as model_checker
import lib.quantity_takeoff as qto


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.filename = None
        self._update_filename_label()

        self.geometry("400x150")

        self.file_button = customtkinter.CTkButton(
            self, text="IFC-Datei auswählen", command=self._select_file
        )
        self.file_button.pack(padx=20, pady=20)

        self.file_label = customtkinter.CTkLabel(master=self, text="")
        self.file_label.pack()

        self.run_button = customtkinter.CTkButton(
            self, text="Datei verarbeiten", state="disabled", command=self._run
        )
        self.run_button.pack(padx=20, pady=20)

        self.progress_bar = customtkinter.CTkProgressBar(self, mode="indeterminate")

    def _select_file(self):
        self.filename = filedialog.askopenfilename(
            title="Bitte eine Datei auswählen", filetypes=[("IFC", "*.ifc")]
        )
        self._update_filename_label()
        self.run_button.configure(state="normal")

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

    def _update_progress_bar(self, operation: str):
        # check if progress bar is already packed
        if not self.progress_bar.winfo_ismapped():
            self.progress_bar.pack()
        if operation == "start":
            self.progress_bar.start()
        elif operation == "stop":
            self.progress_bar.stop()

    def _run(self):
        if not self.filename:
            self.show_error("Keine Datei ausgewählt")
            return
        self._update_progress_bar("start")

        processed_file_path = bbsoft.process(self.filename)
        model_checker.run(processed_file_path)
        qto.get(processed_file_path)

        self._update_progress_bar("stop")


app = App()
app.mainloop()
