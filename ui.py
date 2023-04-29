import customtkinter
from gmail_client import get_emails
import random
import webbrowser

customtkinter.set_appearance_mode("System")  
customtkinter.set_default_color_theme("blue") 

class MyCheckboxFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, values):
        super().__init__(master)
        self.values = sorted(values,key=lambda i: i.lower())
        self.checkboxes = []
        self.make_list()
    
    def make_list(self):
        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, text=value)
            checkbox.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")
            self.checkboxes.append(checkbox)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes
    
    def update_list(self,values):
        self.values = sorted(values,key=lambda i: i.lower())
        self.checkboxes = []
        self.make_list()
        self.update()

    def select_all(self):
        if self.checkboxes[0].get() == 0:
            for checkbox in self.checkboxes:
                checkbox.select()
        else:
            for checkbox in self.checkboxes:
                checkbox.deselect()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Py-Unsubscribe")
        self.iconbitmap("Squarecle.ico")
        self.geometry("400x400")
        self.grid_columnconfigure((0, 2), weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.subscriptions = get_emails()

        self.checkbox_frame = MyCheckboxFrame(self, values=self.subscriptions)
        self.checkbox_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew",columnspan=3)

        self.refresh_button = customtkinter.CTkButton(self, text="Refresh", command=self.refresh_list,fg_color="grey")
        self.refresh_button.grid(row=1, column=0, padx=10, pady=10, sticky="nsew", columnspan=1)

        self.select_all_button = customtkinter.CTkButton(self, text=f"Select All ({len(self.subscriptions)})", command=self.select_all,fg_color="gray")
        self.select_all_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew", columnspan=1)

        self.unsub_button = customtkinter.CTkButton(self, text="Unsubscribe!", command=self.open_unsub_link)
        self.unsub_button.grid(row=1, column=2, padx=10, pady=10, sticky="ew", columnspan=1)

    def refresh_list(self):
        emails = get_emails(random.randint(20,200))
        self.subscriptions = emails
        self.select_all_button.configure(text = f"Select All ({len(self.subscriptions)})")
        self.checkbox_frame.update_list(values=self.subscriptions)
        

    def open_unsub_link(self):
        urls = [links for sender,links in self.subscriptions.items() if sender in self.checkbox_frame.get()]
        print(urls)
        for url in urls:
            if url[0] != "None":
                webbrowser.open(url[0].replace("<","").replace(">",""))

    def select_all(self):
        self.checkbox_frame.select_all()

if __name__ == '__main__':
    app = App()
    app.mainloop()