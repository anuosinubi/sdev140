# Author: Anuoluwapo Osinubi
# Program Goal: The purpose of Kwikaweb Domain Checker application is to provide a graphical user interface (GUI) for checking the availability 
# of domain names and obtaining relevant domain information. It aims to simplify the process of searching for domain availability
# and retrieving essential details for users who are interested in registering or acquiring domain names.

# Import necessary libraries
import tkinter as tk   # tkinter for creating and managing the GUI
import whois   # whois for checking domain availability and fetching domain information
from PIL import Image, ImageTk   # PIL for image manipulation (resize, conversion to PhotoImage, etc.)
import io   # io for reading raw bytes data (used when loading images)
import urllib.request   # urllib for making HTTP requests to fetch images from URLs

class DomainInfoGUI:
    def __init__(self):
        # Initialize main application window
        self.window = tk.Tk() # Creating an instance of Tk class which represents the main window
        self.window.state('zoomed') # Set the initial state of the window as zoomed/full-screen
        self.window.title("Domain Name Search") # Set the title of the window

        # Load and display the application logo
        self.logo_img_url = "https://kwikaweb.com/wp-content/uploads/2023/07/Kwikaweb-PNG.png" # URL of the logo image
        self.logo_img = self.load_image_from_url(self.logo_img_url, (238, 40)) # Call custom function to load the image from URL and resize it
        self.logo_img_label = tk.Label(self.window, image=self.logo_img) # Creating a label to hold the image
        self.logo_img_label.pack(pady=10) # Displaying the label on the window with padding on the y-axis

        # Create a menu bar in the application window
        self.menu = tk.Menu(self.window) # Creating an instance of Menu class
        self.window.config(menu=self.menu) # Adding the menu to the window

        # Adding menu options with their respective command functions
        self.menu.add_command(label="Domain Name Search", command=self.check_domain_availability) # 'Domain Name Search' menu option
        self.menu.add_command(label="WHOIS Lookup", command=self.whois_lookup_window) # 'WHOIS Lookup' menu option

        self.lbl_domain = tk.Label(self.window, text="Search for your Domain Name with ease:") # Creating a label widget for instructing the user.
        self.lbl_domain.pack(pady=10) # Packing it into the window with some padding along the y-axis.

        self.entry_domain = tk.Entry(self.window, width=30) # Creating an entry widget that will be used to capture user input. The domain name that the user wants to search for will be typed here.
        self.entry_domain.pack(pady=5) # Packing it into the window with some padding along the y-axis.

        self.btn_search = tk.Button(self.window, text="Search Availability", command=self.check_domain_availability) # Creating a search button. When clicked, it triggers the check_domain_availability function to verify the availability of the entered domain.
        self.btn_search.pack(pady=10) # Packing it into the window with some padding along the y-axis.

        self.btn_whois = tk.Button(self.window, text="WHOIS Lookup", command=self.whois_lookup_window) # Creating a WHOIS button. When clicked, it triggers the whois_lookup_window function to display a window where the WHOIS information of a domain can be viewed.
        self.btn_whois.pack(pady=10) # Packing it into the window with some padding along the y-axis.

        self.btn_exit = tk.Button(self.window, text="Exit", command=self.exit_app) # Creating an exit button. When clicked, it triggers the exit_app function which closes the application.
        self.btn_exit.pack(pady=10) # Packing it into the window with some padding along the y-axis.

        self.main_window_img_url = "https://kwikaweb.com/wp-content/uploads/2023/07/Domain-Name-Registration-and-Transfer-Image.png" # Setting the URL of the main window image. The URL is where the image file is hosted online.
        self.main_window_img_alt_text = "Domain Name Registration and Transfer Image" # Setting the alternative text for the main window image. This text is useful for accessibility and when the image cannot be loaded.
        self.main_window_img = self.load_image_from_url(self.main_window_img_url, (226, 195), alt_text=self.main_window_img_alt_text) # Calling the function 'load_image_from_url' to fetch and process the image from the provided URL. The function takes the URL, the desired size of the image (226x195 in this case) and the alternative text as parameters.
        self.main_window_img_label = tk.Label(self.window, image=self.main_window_img) # Creating a label widget to display the fetched image in the GUI.
        self.main_window_img_label.pack() # Packing the image label widget into the window.

        self.whois_window = None # Setting 'self.whois_window' to None. This is the initialization for the WHOIS lookup window which will be defined later in the program.

        
    def center_window(self, window): # This function is used to center a given window on the screen
        window.update_idletasks() # First, we update the window's idle tasks to ensure we have the most recent size info
        width = window.winfo_width() # Get the width of the window
        height = window.winfo_height() # Get the height of the window
        # Calculate the position to center the window
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y)) # Set the geometry of the window to center it
    
    def check_domain_availability(self): # This method checks if a domain is available by calling the is_domain_available function. It will open a new window with the result message.
        domain_name = self.entry_domain.get() # Retrieving the domain name from the entry widget.
        availability = self.is_domain_available(domain_name) # Call the function is_domain_available with the domain name to check if it is available.
        
        # If the domain is available, the message will say it is available. If not, it will say it is not available.
        if availability:
            message = f"The domain '{domain_name}' is available!"
        else:
            message = f"The domain '{domain_name}' is not available."

        result_window = tk.Toplevel(self.window) # Create a new toplevel window to show the result message.
        result_window.geometry('300x100') # Set the size of the result window.
        result_label = tk.Label(result_window, text=message) # Create a label with the message text and add it to the result window.
        result_label.pack(pady=10) # Pack the label with a padding in the y direction.

        btn_back = tk.Button(result_window, text="Back To Search", command=result_window.destroy) # Create a button for going back to the search. When this button is pressed, the result window is destroyed.
        btn_back.pack(pady=10) # Pack the button with a padding in the y direction.

        self.center_window(result_window) # Center the result window on the screen.

    # This method checks if a domain is available by using the whois library.
    # It returns True if the domain is available, and False otherwise.
    def is_domain_available(self, domain_name): 
        try:
            # Try to get whois information for the domain. If the domain is taken, this will succeed.
            w = whois.whois(domain_name)
            return False
            # If getting whois information fails with a PywhoisError, this means the domain is available.
        except whois.parser.PywhoisError:
            return True
    
    def whois_lookup_window(self): # This method creates a new window for WHOIS lookup.
        self.whois_window = tk.Toplevel(self.window) # Create a new toplevel window for WHOIS lookup.
        self.whois_window.title("WHOIS Lookup") # Set the title of the WHOIS window.
        self.whois_window.state('zoomed') # Maximize the WHOIS window.

        self.logo_img_label = tk.Label(self.whois_window, image=self.logo_img) # Create a label with the logo image and add it to the WHOIS window.
        self.logo_img_label.pack(pady=10) # Add the label to the window with padding in the y direction.

        self.whois_menu = tk.Menu(self.whois_window) # Create a menu for the WHOIS window.
        self.whois_window.config(menu=self.whois_menu) # Set the menu of the WHOIS window.
        
        # Add commands to the WHOIS window menu.
        self.whois_menu.add_command(label="Domain Name Search", command=self.back_to_main_window) # Go back to the main window for domain name search.
        self.whois_menu.add_command(label="WHOIS Lookup", command=self.whois_lookup_window) # Open the WHOIS lookup window.

        self.whois_lbl_domain = tk.Label(self.whois_window, text="Enter Domain Name") # Create a label prompting the user to enter a domain name.
        self.whois_lbl_domain.pack(pady=10) # Add the label to the window with padding in the y direction.

        self.whois_entry_domain = tk.Entry(self.whois_window, width=30) # Create an entry field for the user to enter a domain name.
        self.whois_entry_domain.pack(pady=5) # Add the entry field to the window with padding in the y direction.

        self.whois_btn_search = tk.Button(self.whois_window, text="Get WHOIS Information", command=self.get_whois_info) # Create a button to initiate the WHOIS lookup.
        self.whois_btn_search.pack(pady=10) # Add the button to the window with padding in the y direction.

        self.whois_btn_back = tk.Button(self.whois_window, text="Domain Name Search", command=self.back_to_main_window) # Create a button to go back to the domain name search.
        self.whois_btn_back.pack(pady=10) # Add the button to the window with padding in the y direction.

        self.whois_btn_exit = tk.Button(self.whois_window, text="Exit", command=self.exit_app) # Create a button to exit the application.
        self.whois_btn_exit.pack(pady=10) # Add the button to the window with padding in the y direction.

        self.whois_window_img_url = "https://kwikaweb.com/wp-content/uploads/2023/07/Domain-Name-Registration-Image.png" # Define the URL of the image to be loaded for the WHOIS lookup window.
        self.whois_window_img_alt_text = "WHOIS Lookup Image" # Set an alternate text for the image. This is typically used for accessibility purposes.
        self.whois_window_img = self.load_image_from_url(self.whois_window_img_url, (226, 195), alt_text=self.whois_window_img_alt_text)  # Use the helper function load_image_from_url() to load the image from the provided URL. The image is resized to the dimensions (226, 195), and the alternate text is also set.
        self.whois_window_img_label = tk.Label(self.whois_window, image=self.whois_window_img) # Create a Tkinter Label widget, set the image loaded from the URL as the label's image, and assign this label to the 'whois_window_img_label' attribute.
        self.whois_window_img_label.pack() # Pack (position) the label widget in the window with default settings (centered alignment).

    def get_whois_info(self): # This method retrieves WHOIS information for a given domain.
        domain_name = self.whois_entry_domain.get() # Get the domain name from the entry field.
        w = whois.whois(domain_name) # Retrieve the WHOIS information for the domain.

        whois_info_window = tk.Toplevel(self.whois_window) # Create a new toplevel window to display the WHOIS information.
        whois_info_window.geometry('500x350') # Set the size of the window.

        lbl_whois = tk.Label(whois_info_window, text="WHOIS information of "+ domain_name +": ") # Create a label to display the domain name.
        lbl_whois.pack(pady=10) # Add the label to the window with padding in the y direction.

        txt_whois = tk.Text(whois_info_window, height=15, width=70) # Create a text box to display the WHOIS information.
        txt_whois.pack(pady=5) # Add the text box to the window with padding in the y direction.
        txt_whois.insert(tk.END, str(w)) # Insert the WHOIS information into the text box.

        btn_back = tk.Button(whois_info_window, text="Back To Search", command=whois_info_window.destroy) # Create a button to close the WHOIS information window and go back to search.
        btn_back.pack(pady=10) # Add the button to the window with padding in the y direction.

        self.center_window(whois_info_window) # Center the WHOIS information window on the screen.

    def exit_app(self): # This method closes the main application window.
        self.window.destroy() # Destroy the main application window.

    def back_to_main_window(self): # This method closes the WHOIS lookup window and goes back to the main window.
        self.whois_window.destroy() # Destroy the WHOIS lookup window.
        
        # Function to fetch an image from a URL and convert it to a PhotoImage after resizing
    def load_image_from_url(self, url, size=None, alt_text=None):
        # First, we read the raw data from the URL
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        # Then, we open the image from the raw data and resize it
        im = Image.open(io.BytesIO(raw_data))
        if size is not None:
            im = im.resize(size, Image.BICUBIC)
        # Finally, we convert the image object to a PhotoImage and return it
        image = ImageTk.PhotoImage(im)
        if alt_text is not None:
            image.alt = alt_text
        return image

domain_info_gui = DomainInfoGUI() # Create an instance of the DomainInfoGUI class
domain_info_gui.window.mainloop() # Start the main event loop of the application