# Author: Anuoluwapo Osinubi
# Program Goal: The purpose of Kwikaweb Domain Checker application is to provide a graphical user interface (GUI) for checking the availability 
# of domain names and obtaining relevant domain information. It aims to simplify the process of searching for domain availability
# and retrieving essential details for users who are interested in registering or acquiring domain names.

import tkinter as tk
import whois
from PIL import Image, ImageTk
import io
import urllib.request

class DomainInfoGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.state('zoomed')
        self.window.title("Domain Information")

        self.logo_img_url = "https://kwikaweb.com/wp-content/uploads/2023/07/Kwikaweb-PNG.png"
        self.logo_img = self.load_image_from_url(self.logo_img_url, (238, 40))
        self.logo_img_label = tk.Label(self.window, image=self.logo_img)
        self.logo_img_label.pack(pady=10)

        self.menu = tk.Menu(self.window)
        self.window.config(menu=self.menu)

        self.menu.add_command(label="Domain Name Search", command=self.check_domain_availability)
        self.menu.add_command(label="WHOIS Lookup", command=self.whois_lookup_window)

        self.lbl_domain = tk.Label(self.window, text="Search for your Domain Name with ease:")
        self.lbl_domain.pack(pady=10)

        self.entry_domain = tk.Entry(self.window, width=30)
        self.entry_domain.pack(pady=5)

        self.btn_search = tk.Button(self.window, text="Search Availability", command=self.check_domain_availability)
        self.btn_search.pack(pady=10)

        self.btn_exit = tk.Button(self.window, text="Exit", command=self.exit_app)
        self.btn_exit.pack(pady=10)

        # Load image from URL for main window
        self.main_window_img_url = "https://kwikaweb.com/wp-content/uploads/2023/07/Domain-Name-Registration-and-Transfer-Image.png"
        self.main_window_img = self.load_image_from_url(self.main_window_img_url, (226, 195))
        self.main_window_img_label = tk.Label(self.window, image=self.main_window_img)
        self.main_window_img_label.pack()

        self.whois_window = None

    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def check_domain_availability(self):
        domain_name = self.entry_domain.get()
        availability = self.is_domain_available(domain_name)

        if availability:
            message = f"The domain '{domain_name}' is available!"
        else:
            message = f"The domain '{domain_name}' is not available."

        result_window = tk.Toplevel(self.window)
        result_window.geometry('300x100')
        result_label = tk.Label(result_window, text=message)
        result_label.pack(pady=10)
        
        btn_back = tk.Button(result_window, text="Back To Search", command=result_window.destroy)
        btn_back.pack(pady=10)

        self.center_window(result_window)

    def is_domain_available(self, domain_name):
        try:
            w = whois.whois(domain_name)
            return False
        except whois.parser.PywhoisError:
            return True

    def whois_lookup_window(self):
        self.whois_window = tk.Toplevel(self.window)
        self.whois_window.title("WHOIS Lookup")
        self.whois_window.state('zoomed')

        self.logo_img_label = tk.Label(self.whois_window, image=self.logo_img)
        self.logo_img_label.pack(pady=10)

        self.whois_menu = tk.Menu(self.whois_window)
        self.whois_window.config(menu=self.whois_menu)

        self.whois_menu.add_command(label="Domain Name Search", command=self.back_to_main_window)
        self.whois_menu.add_command(label="WHOIS Lookup", command=self.whois_lookup_window)

        self.whois_lbl_domain = tk.Label(self.whois_window, text="Enter Domain Name")
        self.whois_lbl_domain.pack(pady=10)

        self.whois_entry_domain = tk.Entry(self.whois_window, width=30)
        self.whois_entry_domain.pack(pady=5)

        self.whois_btn_search = tk.Button(self.whois_window, text="Get WHOIS Information", command=self.get_whois_info)
        self.whois_btn_search.pack(pady=10)

        self.whois_btn_back = tk.Button(self.whois_window, text="Go Back", command=self.back_to_main_window)
        self.whois_btn_back.pack(pady=10)

        # Load image from URL for whois window
        self.whois_window_img_url = "https://kwikaweb.com/wp-content/uploads/2023/07/Domain-Name-Registration-Image.png"
        self.whois_window_img = self.load_image_from_url(self.whois_window_img_url, (226, 195))
        self.whois_window_img_label = tk.Label(self.whois_window, image=self.whois_window_img)
        self.whois_window_img_label.pack()

    def get_whois_info(self):
        domain_name = self.whois_entry_domain.get()
        w = whois.whois(domain_name)

        whois_info_window = tk.Toplevel(self.whois_window)
        whois_info_window.geometry('500x350')

        lbl_whois = tk.Label(whois_info_window, text="WHOIS information of "+ domain_name +": ")
        lbl_whois.pack(pady=10)

        txt_whois = tk.Text(whois_info_window, height=15, width=70)
        txt_whois.pack(pady=5)
        txt_whois.insert(tk.END, str(w))

        btn_back = tk.Button(whois_info_window, text="Back To Search", command=whois_info_window.destroy)
        btn_back.pack(pady=10)
        
        self.center_window(whois_info_window)

    def exit_app(self):
        self.window.destroy()

    def back_to_main_window(self):
        self.whois_window.destroy()

    def load_image_from_url(self, url, size=None):
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        im = Image.open(io.BytesIO(raw_data))
        if size is not None:
            im = im.resize(size, Image.BICUBIC)
        image = ImageTk.PhotoImage(im)
        return image

domain_info_gui = DomainInfoGUI()
domain_info_gui.window.mainloop()