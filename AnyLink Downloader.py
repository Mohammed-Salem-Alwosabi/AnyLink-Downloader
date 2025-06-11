import tkinter as tk
from tkinter import filedialog, messagebox
import yt_dlp
import threading
import os
import customtkinter
from PIL import Image, ImageTk
import cv2 
import subprocess
import sys
import webbrowser

class AnyLinkDownloaderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("AnyLink Downloader")

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        window_width = 700
        window_height = 700
        x_coordinate = (screen_width / 2) - (window_width / 2)
        y_coordinate = (screen_height / 2) - (window_height / 2)
        self.master.geometry(f"{window_width}x{window_height}+{int(x_coordinate)}+{int(y_coordinate)}")
        self.master.resizable(False, False)

        try:
            self.master.iconbitmap("images/AnyLink Downloader Logo.ico")
        except tk.TclError :
            pass

        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("blue")

        #? ------------------------ My Links Frame -----------------------
        self.u_face = 'https://www.facebook.com/profile.php?id=61551057515420&mibextid=9R9pXO'
        self.u_ins = 'https://instagram.com/karzma_co.ms?igshid=MzMyNGUyNmU2YQ=='
        self.u_tele = 'https://t.me/KaRZMa_Code'
        
        self.my_whatsapp = "https://wa.me/+967739003665"
        self.my_linkedin = 'https://www.linkedin.com/in/mohammed-salem-ali-alwosabi-842757321?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app'
        self.my_face = 'https://www.facebook.com/share/1EetzPibZt/'
        self.my_ins = 'https://www.instagram.com/m.salem_hy?igsh=MTYzeXk5emJpcmV3Ng== '
        self.my_tele = 'http://t.me/MohammedAlwosabi'
        self.my_thre = 'https://www.threads.net/@m.salem_hy'
        #? ------------------------ My Links Frame -----------------------
        
        
        #todo --- SPLASH SCREEN FRAME ---
        self.splash_frame = customtkinter.CTkFrame(master, corner_radius=0)
        self.splash_frame.pack(fill=tk.BOTH, expand=True)

        # Video playback setup
        self.splash_video_path = "images/AnyLink Download Dark Video HK.mp4"
        self.cap = None
        self.current_frame_image = None # To hold the CTkImage for the current frame

        self.splash_label = customtkinter.CTkLabel(self.splash_frame, text="") 
        self.splash_label.pack(expand=True)

        # Start video playback in a thread
        # Schedule the main window to appear after 4 seconds (4000 milliseconds)
        self.master.after(4000, self.hide_splash_and_show_main) # MODIFIED LINE
        self.master.after(300, self.start_splash_video) # Start video shortly after to allow UI to render
        #todo --- END SPLASH SCREEN FRAME ---


        # --- Main Application Frames (initialize but not pack yet) ---
        self.head_frame = customtkinter.CTkFrame(master, fg_color="transparent")
        self.main_frame = customtkinter.CTkFrame(master, corner_radius=10)
        self.theme_frame = customtkinter.CTkFrame(master, fg_color="transparent")

        
        #todo --- MENU BAR IMPLEMENTATION START ---
        self.menubar = tk.Menu(master, 
                               bg="black", 
                               fg="white", 
                               activebackground="#444444", # Darker grey for hover effect
                               activeforeground="white",
                               relief="flat", # Flat appearance
                               borderwidth=0 # No border
                              )

        # File Menu
        self.file_menu = tk.Menu(self.menubar, tearoff=0, 
                                  bg="white", 
                                  fg="black", 
                                  activebackground="#444444", 
                                  activeforeground="white",
                                  relief="flat",
                                  borderwidth=0
                                 )
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open Download Folder", command=None)
        self.file_menu.add_separator() # horizontal line separator
        self.file_menu.add_command(label="Exit", command=master.destroy)

        # Help Menu
        self.help_menu = tk.Menu(self.menubar, tearoff=0, 
                                  bg="white", 
                                  fg="black", 
                                  activebackground="#444444", 
                                  activeforeground="white",
                                  relief="flat",
                                  borderwidth=0
                                 )
        self.menubar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="WhatsApp us", command=self.open_whatsapp)
        self.help_menu.add_command(label="Report a problem", command=self.open_bug_report)
        self.help_menu.add_separator()
        self.help_menu.add_command(label="About", command=self.show_about_app_details)

        # Contact us Menu
        self.contact_us_menu = tk.Menu(self.menubar, tearoff=0, 
                                  bg="white", 
                                  fg="black", 
                                  activebackground="#444444", 
                                  activeforeground="white",
                                  relief="flat",
                                  borderwidth=0
                                 )
        self.menubar.add_cascade(label="Contact us", menu=self.contact_us_menu)
        self.contact_us_menu.add_command(label="Email Support", command=self.open_email_support)
        self.contact_us_menu.add_command(label="Report a Bug", command=self.open_bug_report)
        self.contact_us_menu.add_command(label="Follow Our Telegram Channel", command=lambda: self.open_url(self.u_tele))
        
        #todo --- MENU BAR IMPLEMENTATION END ---

        # Switch for Dark and Light Mode
        self.switch_var = customtkinter.StringVar(value="Dark") # Initialize with "Dark"
        my_switch = customtkinter.CTkSwitch(
            master=self.head_frame,
            text="Light Mode",
            command=lambda: self.set_app_appearance_mode(self.switch_var.get()),
            variable=self.switch_var,
            onvalue="Light",  # Custom 'on' value
            offvalue="Dark", # Custom 'off' value
            corner_radius=10,
            fg_color=("gray", "darkgray"), # Different colors for light/dark mode
            button_color="white",
            button_hover_color="lightblue",
            font=("Arial", 14, "bold"),
            state="normal"
        )
        my_switch.pack(side=tk.LEFT,pady=2)
        #? ------------ ---
        
        
        # Entry Field
        self.url_label = customtkinter.CTkLabel(self.main_frame, text="Video Link (URL):", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.url_entry = customtkinter.CTkEntry(self.main_frame, width=550, height=35, placeholder_text="Enter AnyLink video URL here", font=customtkinter.CTkFont(size=12))
        
        
        # Download Path Field
        self.path_label = customtkinter.CTkLabel(self.main_frame, text="Download Path:", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.path_entry = customtkinter.CTkEntry(self.main_frame, width=470, height=35, font=customtkinter.CTkFont(size=12))
        self.browse_button = customtkinter.CTkButton(self.main_frame, text="Browse", command=self.browse_path, width=70, height=35)
        
        #? will set the Download Field as a defualt path
        default_download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        if not os.path.isdir(default_download_dir):
            default_download_dir = os.path.expanduser("~")
        self.path_entry.insert(0, default_download_dir)
        
        
        # Video Quality Field
        self.quality_label = customtkinter.CTkLabel(self.main_frame, text="Select Quality:", font=customtkinter.CTkFont(size=13, weight="bold"))        
        self.quality_options = [
            "720p (Auto)",
            "1080p",
            "720p",
            "360p"
        ]
        self.selected_quality_var = customtkinter.StringVar(value=self.quality_options[0]) # Default to "720p (Auto)"
        self.quality_combobox = customtkinter.CTkOptionMenu(self.main_frame,
                                                          dropdown_fg_color="#285B91",
                                                          values=self.quality_options,
                                                          variable=self.selected_quality_var,
                                                          font=customtkinter.CTkFont(size=12),
                                                          state="readonly") # Make it read-only
        
        
        # Download Type Field
        self.type_label = customtkinter.CTkLabel(self.main_frame, text="Download Type:", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.download_type_var = customtkinter.StringVar(value="Video")
        
        
        """# Radio Buttons for Download Type
        self.video_radiobutton = customtkinter.CTkRadioButton(
            self.main_frame,
            text="Video",
            variable=self.download_type_var,
            value="Video",
            font=customtkinter.CTkFont(size=12)
        )
        self.audio_radiobutton = customtkinter.CTkRadioButton(
            self.main_frame,
            text="Audio",
            variable=self.download_type_var,
            value="Audio",
            font=customtkinter.CTkFont(size=12)
        )"""
         
        self.download_type_optionmenu = customtkinter.CTkOptionMenu(self.main_frame, values=["Video", "Audio"],
                                                        variable=self.download_type_var,
                                                        font=customtkinter.CTkFont(size=12))
        
        
        try:
            self.download_icon_light = customtkinter.CTkImage(
                light_image=Image.open("images/Download Button.png"), 
                dark_image=Image.open("images/Download Button.png"), 
                size=(25, 25) 
            )
        except FileNotFoundError:
            messagebox.showwarning("Warning: download_icon.png not found. Download button will not have an image.")
            self.download_icon_light = None 
        
        # Download Button
        self.download_button = customtkinter.CTkButton(self.main_frame, text="Download", command=self.start_download,
                                                       image=self.download_icon_light, # Assign the CTkImage
                                                       compound="left", # Image on the left of text (optional, default is left)
                                                       height=40,
                                                       font=customtkinter.CTkFont(size=14, weight="bold"),
                                                       fg_color="#4CAF50", hover_color="#45a049")
        
        # Status label
        self.status_label = customtkinter.CTkLabel(self.main_frame, text="Ready", font=customtkinter.CTkFont(size=11, slant="italic"))
        
        # Progress Bar
        self.progress_bar = customtkinter.CTkProgressBar(self.main_frame, height=15)
        self.progress_bar.set(0)



        try:
            self.information_button_icon = customtkinter.CTkImage(
                light_image=Image.open("images/Information_icon.png"),
                dark_image=Image.open("images/Information_icon.png"),
                size=(20, 20) )
        except FileNotFoundError:
            messagebox.showwarning("Warning: Inforamtion_icon.png not found. Information button will not have an image.")
            self.information_button_icon = None
            
           
        # Information Button
        self.information_button = customtkinter.CTkButton(
            master=self.theme_frame,
            text="Info center",
            image=self.information_button_icon, 
            compound="left", 
            command=self.show_info_window,
            width=100,
            height=30,
            corner_radius=5,
            font=customtkinter.CTkFont(size=12, weight="bold")
        )
        self.information_button.pack(side=tk.LEFT, padx=5)
        
        
        # Close Button
        self.close_button = customtkinter.CTkButton(self.theme_frame, text="Close",command=self.master.destroy, width=100, height=30,fg_color="red", hover_color="darkred")
        self.close_button.pack(side=tk.RIGHT, padx=5)

        self.update_status("Ready")
        
        
    #! ----------------------------------------------- Functions Start Here -----------------------------------------------
    
    
    def open_email_support(self):
        """Opens the default email client to send an email to support."""
        support_email = "m.salem.alwosabi@gmail.com" 
        subject = "AnyLink Downloader Support Request"
        body = "Dear Support Team,\n\n" \
               "I am writing regarding the AnyLink Downloader application.\n\n" \
               "My operating system is: {}\n" \
               "Application Version: 1.0\n\n" \
               "Please describe your issue or question below:\n\n" \
               "----------------------------------------------------\n\n".format(sys.platform)

        try:
            webbrowser.open(f"mailto:{support_email}?subject={subject}&body={body}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open email client. Please email us at: {support_email}\n\nDetails: {e}")
    
    def open_bug_report(self):
        bug_report_url = "https://forms.gle/iPtDeCjekHsPZkgv6" 
        try:
            webbrowser.open_new_tab(bug_report_url)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open bug report link. Please contact us: +967 739 003 665 .\n\nDetails: {e}")
    
    def show_ask_help_dialog(self):
        """Displays a dialog box with information on how to get help."""
        help_message = "Need Assistance?\n\n" \
                       "For help, please visit our online documentation or support forum.\n" \
                       "You can also contact our support team via email.\n\n" \
                       "Website: \n" \
                       "Email: m.salem.alwosabi@gmail.com"
        messagebox.showinfo("Ask Help", help_message)
    
    def start_splash_video(self):
        self.cap = cv2.VideoCapture(self.splash_video_path)
        if not self.cap.isOpened():
            messagebox.showerror("Error", f"Could not open video file: {self.splash_video_path}")
            self.hide_splash_and_show_main()
            return

        self.video_duration_ms = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT) * 1000 / self.cap.get(cv2.CAP_PROP_FPS))
        self.play_video_frame()

    def play_video_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert the image from BGR color (which OpenCV uses) to RGB color
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img_pil = Image.fromarray(cv2image)


            self.current_frame_image = customtkinter.CTkImage(img_pil, size=(self.master.winfo_width(), self.master.winfo_height()))
            self.splash_label.configure(image=self.current_frame_image)
            self.splash_label.image = self.current_frame_image

            self.master.after(20, self.play_video_frame) 
        else:
            self.cap.release()
            self.hide_splash_and_show_main()

    def hide_splash_and_show_main(self):
        if self.cap:
            self.cap.release()

        self.splash_frame.pack_forget()

        # Pack the Head application frame
        self.head_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=(10, 0))
        # Pack the main application frame
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        # Grid the components within main_frame
        self.url_label.grid(row=0, column=0, sticky="w", pady=(15, 5), padx=15)
        self.url_entry.grid(row=1, column=0, columnspan=2, pady=(0, 20), padx=15, sticky="ew")
        self.path_label.grid(row=2, column=0, sticky="w", pady=(15, 5), padx=15)
        self.path_entry.grid(row=3, column=0, pady=(0, 20), padx=15, sticky="ew")
        self.browse_button.grid(row=3, column=1, pady=(0, 20), padx=(0, 15), sticky="e")
        self.quality_label.grid(row=4, column=0, columnspan=2, pady=(10, 5), padx=10, sticky="w") 
        self.quality_combobox.grid(row=5, column=0, columnspan=2, pady=5, padx=10, sticky="ew") 
        self.type_label.grid(row=6, column=0, sticky="w", pady=(15, 5), padx=15)
        self.download_type_optionmenu.grid(row=7, column=0, columnspan=2, pady=(0, 25), padx=15 ,sticky="ew")
        #self.video_radiobutton.grid(row=7, column=0,padx=35, pady=10,sticky="ew")
        #self.audio_radiobutton.grid(row=7, column=1, padx=(15,15), pady=10,sticky="ew")
        self.download_button.grid(row=8, column=0, columnspan=2, pady=(15, 15), padx=15, sticky="ew")
        self.status_label.grid(row=9, column=0, columnspan=2, pady=(5, 5), padx=15, sticky="ew")
        self.progress_bar.grid(row=10, column=0, columnspan=2, pady=(5, 0), padx=15, sticky="ew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=0)
         
        """self.main_frame.grid_rowconfigure(0, weight=0) # URL Label
        self.main_frame.grid_rowconfigure(1, weight=0) # URL Entry
        self.main_frame.grid_rowconfigure(2, weight=0) # Download Type Radio Buttons
        self.main_frame.grid_rowconfigure(3, weight=0) # Path Label (Original)
        self.main_frame.grid_rowconfigure(4, weight=0) # Path Entry (Original)
        self.main_frame.grid_rowconfigure(5, weight=0) # Corrected row for Path Label
        self.main_frame.grid_rowconfigure(6, weight=0) # Corrected row for Path Entry and Browse Button
        self.main_frame.grid_rowconfigure(7, weight=0)# NEW: Quality Label
        self.main_frame.grid_rowconfigure(8, weight=0) # NEW: Quality ComboBox
        self.main_frame.grid_rowconfigure(9, weight=0) # Download Button (shifted from 7 to 9)
        self.main_frame.grid_rowconfigure(10, weight=0) # Progress Bar (shifted from 8 to 10)
        self.main_frame.grid_rowconfigure(11, weight=1) # Status Label (expands, shifted from 9 to 11)"""


        # Pack the theme frame and language frame
        self.theme_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=(0, 10))

        # it will show the menu bar 
        self.master.config(menu=self.menubar)
        
        # Ensure the window is visible and focused
        self.master.deiconify()
        self.master.focus_force()
        self.master.update_idletasks()

    def set_app_appearance_mode(self, mode_string):
        #*Sets the CustomTkinter appearance mode (Light, Dark, System)
        customtkinter.set_appearance_mode(mode_string)
        current_mode = customtkinter.get_appearance_mode()
        if current_mode == "Dark":
            self.status_label.configure(text_color="#00FF00")
        else:
            self.status_label.configure(text_color="#008000")

    def browse_path(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder_selected)

    def update_status(self, message, is_error=False):
        self.status_label.configure(text=message)
        if is_error:
            self.status_label.configure(text_color="red")
        else:
            current_mode = customtkinter.get_appearance_mode()
            if current_mode == "Dark":
                self.status_label.configure(text_color="#00FF00")
            else:
                self.status_label.configure(text_color="#008000")
        self.master.update_idletasks()

    def download_progress_hook(self, d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded_bytes = d.get('downloaded_bytes')
            if total_bytes and downloaded_bytes:
                percent = (downloaded_bytes / total_bytes)
                self.progress_bar.set(percent)
                self.update_status(f"Downloading: {d['_percent_str']} of {d['_total_bytes_str']} at {d['_speed_str']}")
            else:
                self.update_status(f"Downloading: {d['_percent_str']}")
        elif d['status'] == 'finished':
            self.progress_bar.set(1)
            self.update_status("Download finished, processing...")
        elif d['status'] == 'error':
            self.progress_bar.set(0)
            self.update_status("Download failed!", is_error=True)
            messagebox.showerror("Error", f"Download failed: {d.get('error', 'Unknown error')}")

    def download_video_audio(self):
        url = self.url_entry.get()
        download_path = self.path_entry.get()
        download_type = self.download_type_var.get()
        selected_quality = self.selected_quality_var.get()
        
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL.")
            self.update_status("Error: URL missing.", is_error=True)
            return
        if not download_path:
            messagebox.showerror("Error", "Please select a download path.")
            self.update_status("Error: Download path missing.", is_error=True)
            return

        if not os.path.isdir(download_path):
            try:
                os.makedirs(download_path)
            except OSError as e:
                messagebox.showerror("Error", f"Could not create download directory: {e}")
                self.update_status("Error: Directory creation failed.", is_error=True)
                return

        self.update_status("Starting download...")
        self.download_button.configure(state="disabled")
        self.progress_bar.set(0)

        try:
            ydl_opts = {
                'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
                'progress_hooks': [self.download_progress_hook],
                'ignoreerrors': False,
                'noplaylist': True,
            }

            if download_type == "Video":
                if selected_quality == "720p (Auto)":
                    ydl_opts['format'] = 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'
                elif selected_quality == "1080p":
                    # Tries to get 1080p MP4 video, then best audio, merges to MP4.
                    ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best'
                elif selected_quality == "720p":
                    # Tries to get 720p MP4 video, then best audio, merges to MP4.
                    ydl_opts['format'] = 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'
                elif selected_quality == "360p":
                    # Tries to get 360p MP4 video, then best audio, merges to MP4.
                    ydl_opts['format'] = 'bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'
                else: # Fallback for unexpected selection or "Best (Auto)" default
                    ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best'
                
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }]

            elif download_type == "Audio":
                if selected_quality == "Audio (MP3 320kbps)":
                    ydl_opts['format'] = 'bestaudio/best'
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '320', # High quality MP3
                    }]
                else :
                    ydl_opts['format'] = 'bestaudio/best'
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192', # Medium quality MP3
                    }]
                

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                self.progress_bar.set(1)
                self.update_status("Download and processing complete!")
                messagebox.showinfo("Success", "Video/Audio downloaded successfully!")

        except yt_dlp.utils.DownloadError as e:
            self.update_status(f"Download Error: {e}", is_error=True)
            messagebox.showerror("Download Error", f"Download failed: {e}")
        except Exception as e:
            self.update_status(f"An unexpected error occurred: {e}", is_error=True)
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        finally:
            self.download_button.configure(state="normal")

    def start_download(self):
        download_thread = threading.Thread(target=self.download_video_audio)
        download_thread.start()
    
    def open_whatsapp(self):
        phone_number = "+967739003665"
        message = "Hello Mr.Mohammed Salem Alwosabi, I need some help.."  # initial message
        whatsapp_url = f"https://api.whatsapp.com/send?phone={phone_number}&text={message}"
        webbrowser.open(whatsapp_url)
    
    # --- Helper function to open URLs ---
    def open_url(self, url):
        try:
            webbrowser.open_new_tab(url)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open link: {e}")

    # --- New function to open About Application details (sub-window) ---
    def show_about_app_details(self):
        about_app_window = customtkinter.CTkToplevel(self.master)
        about_app_window.title("About AnyLink Downloader")
        about_app_window.geometry("500x400")
        about_app_window.resizable(False, False)
        try:
            about_app_window.iconbitmap("images/AnyLink Downloader Logo.ico") 
        except tk.TclError:
            pass
        
        # Center the about app window relative to the main window
        self.master.update_idletasks()
        main_x = self.master.winfo_x()
        main_y = self.master.winfo_y()
        main_width = self.master.winfo_width()
        main_height = self.master.winfo_height()

        about_width = 600
        about_height = 600
        x_coordinate = main_x + (main_width // 2) - (about_width // 2)
        y_coordinate = main_y + (main_height // 2) - (about_height // 2)
        about_app_window.geometry(f"{about_width}x{about_height}+{int(x_coordinate)}+{int(y_coordinate)}")
        
        customtkinter.set_appearance_mode(customtkinter.get_appearance_mode()) # Match theme

        about_title = customtkinter.CTkLabel(about_app_window, text="AnyLink Downloader", font=customtkinter.CTkFont(size=20, weight="bold"))
        about_title.pack(pady=15, padx=20)

        app_info_text = (
            "Version: 1.0.0\n"
            "Developed by: KaRZMa Code, Developer: Mohammed Salem Alwosabi\n\n"
            "AnyLink Downloader is a versatile tool designed to simplify media downloads "
            "from various online platforms. Whether it's a video from YouTube or audio "
            "from a music sharing site, AnyLink Downloader aims to provide a fast and "
            "reliable experience.\n\n"
            "Key Features:\n"
            "- Download videos and audio from supported URLs.\n"
            "- Choose preferred download quality.\n"
            "- Intuitive and user-friendly interface."
        )
        
        about_text_label = customtkinter.CTkLabel(about_app_window, 
                                                  text=app_info_text,
                                                  font=customtkinter.CTkFont(size=15),
                                                  wraplength=450, 
                                                  justify="left")
        about_text_label.pack(pady=10, padx=20)
        
        
        self.close_button = customtkinter.CTkButton(about_app_window, text="Close",command=about_app_window.destroy, width=100, height=30,fg_color="red", hover_color="darkred")
        self.close_button.pack(side=tk.BOTTOM, pady=15)

        about_app_window.grab_set()
        self.master.wait_window(about_app_window)

    
    def show_about_developer(self):
        about_developer_window = customtkinter.CTkToplevel(self.master)
        about_developer_window.title("About Developer")
        about_developer_window.geometry("500x500")
        about_developer_window.resizable(False, False)
        

        self.master.update_idletasks()
        main_x = self.master.winfo_x()
        main_y = self.master.winfo_y()
        main_width = self.master.winfo_width()
        main_height = self.master.winfo_height()

        about_width = 500
        about_height = 500
        x_coordinate = main_x + (main_width // 2) - (about_width // 2)
        y_coordinate = main_y + (main_height // 2) - (about_height // 2)
        about_developer_window.geometry(f"{about_width}x{about_height}+{int(x_coordinate)}+{int(y_coordinate)}")
        try:
            about_developer_window.iconbitmap("images/AnyLink Downloader Logo.ico")
        except tk.TclError:
            pass
        customtkinter.set_appearance_mode(customtkinter.get_appearance_mode()) 

        about_title = customtkinter.CTkLabel(about_developer_window, text="About Developer", font=customtkinter.CTkFont(size=20, weight="bold"))
        about_title.pack(pady=15, padx=20)

        text_frame = customtkinter.CTkFrame(about_developer_window, corner_radius=10)
        text_frame.pack(pady=15, padx=20)

        label_font = customtkinter.CTkFont(size=17)
        label_pady = 5
        label_padx = 15
        
        try:
            personal_facebook_icon = customtkinter.CTkImage(Image.open("images/Facebook_icon.png"), size=(30, 30))
            personal_instagram_icon = customtkinter.CTkImage(Image.open("images/Instegram_icon.png"), size=(30, 30))
            contact_us_icon = customtkinter.CTkImage(Image.open("images/contact_us_icon.png"), size=(30, 30))
            email_icon = customtkinter.CTkImage(Image.open("images/Email_icon.png"), size=(30, 30))
            linkedin_icon = customtkinter.CTkImage(Image.open("images/LinkedIn_icon.png"), size=(30, 30))
        except FileNotFoundError:
            personal_facebook_icon = personal_instagram_icon = contact_us_icon = email_icon = linkedin_icon = None
            
            
        # Developer Name
        customtkinter.CTkLabel(text_frame, text="Developer: Mohammed Salem Alwosabi", font=label_font,
                                justify="left").grid(row=0, column=0, columnspan=2, pady=label_pady, padx=label_padx, sticky="w")

        # Email
        customtkinter.CTkLabel(text_frame, text="Email: m.salem.alwosabi@gmail.com",image=email_icon, compound="left", font=label_font,
                                justify="left").grid(row=1, column=0, columnspan=2, pady=label_pady, padx=label_padx, sticky="w")

        # Contact Number
        customtkinter.CTkLabel(text_frame, text="Contact: +967 739 003 665", image=contact_us_icon, compound="left", font=label_font,
                                justify="left").grid(row=2, column=0, columnspan=2, pady=label_pady, padx=label_padx, sticky="w")
        

        if personal_facebook_icon:
            customtkinter.CTkLabel(text_frame, text="الوصابي سالم محمد", image=personal_facebook_icon, compound="left",
                                   font=label_font, justify="left").grid(row=3, column=0, columnspan=2, pady=label_pady, padx=label_padx, sticky="w")
        else:
            customtkinter.CTkLabel(text_frame, text="الوصابي سالم محمد", font=label_font,
                                   justify="left").grid(row=3, column=0, columnspan=2, pady=label_pady, padx=label_padx, sticky="w")
        
        if personal_instagram_icon:
            customtkinter.CTkLabel(text_frame, text="m.salem_hy", image=personal_instagram_icon, compound="left",
                                   font=label_font, justify="left").grid(row=4, column=0, columnspan=2, pady=label_pady, padx=label_padx, sticky="w")
        else:
            customtkinter.CTkLabel(text_frame, text="m.salem_hy", font=label_font,
                                   justify="left").grid(row=4, column=0, columnspan=2, pady=label_pady, padx=label_padx, sticky="w")
            
        customtkinter.CTkLabel(text_frame, text="Mohammed Salem Ali Alwosabi", image=linkedin_icon, compound="left", font=label_font,
                                justify="left").grid(row=5, column=0, columnspan=2, pady=label_pady, padx=label_padx, sticky="w")
        
        
        self.close_button = customtkinter.CTkButton(about_developer_window, text="Close",command=about_developer_window.destroy, width=100, height=30,fg_color="red", hover_color="darkred")
        self.close_button.pack(side=tk.BOTTOM, pady=15)

        
        about_developer_window.grab_set()
        self.master.wait_window(about_developer_window)

    # --- show_info_window function ---
    def show_info_window(self):
        self.info_window = customtkinter.CTkToplevel(self.master)
        self.info_window.title("Contact & Information")
        self.info_window.geometry("700x650") 
        self.info_window.resizable(False, False) 
        try:
            self.info_window.iconbitmap("images/AnyLink Downloader Logo.ico")
        except tk.TclError:
            pass
                
        # Center the info window relative to the main window
        self.master.update_idletasks() 
        main_x = self.master.winfo_x()
        main_y = self.master.winfo_y()
        main_width = self.master.winfo_width()
        main_height = self.master.winfo_height()

        info_width = 700
        info_height = 750
        x_coordinate = main_x + (main_width // 2) - (info_width // 2)
        y_coordinate = main_y + (main_height // 2) - (info_height // 2)
        self.info_window.geometry(f"{info_width}x{info_height}+{int(x_coordinate)}+{int(y_coordinate)}")
        
        customtkinter.set_appearance_mode(customtkinter.get_appearance_mode()) 


        # Configure grid for the info_window
        self.info_window.grid_columnconfigure(0, weight=1) # Allow column to expand
        self.info_window.grid_rowconfigure(0, weight=0) # Image Frame (fixed size)
        self.info_window.grid_rowconfigure(1, weight=1) # Button Frame (can expand)
        self.info_window.grid_rowconfigure(2, weight=1) # Text Frame (can expand)


        # --- 1. Image Frame (My Company Logo) ---
        image_frame = customtkinter.CTkFrame(self.info_window, corner_radius=10)
        image_frame.grid(row=0, column=0, pady=10, padx=20, sticky="ew")
        image_frame.grid_columnconfigure(0, weight=1) # Center content

        try:
            company_logo = customtkinter.CTkImage(
                light_image=Image.open("images/karzma logo 2.jpg"),
                dark_image=Image.open("images/karzma logo 2.jpg"), 
                size=(350, 350) 
            )
            company_logo_label = customtkinter.CTkLabel(image_frame, image=company_logo, text="")
            company_logo_label.pack(pady=10, padx=10)
        except FileNotFoundError:
            company_logo_label = customtkinter.CTkLabel(image_frame, text="[Company Logo Placeholder]", font=customtkinter.CTkFont(size=14))
            company_logo_label.pack(pady=10, padx=10)

        # --- 2. Button Frame (Social Media & About) ---
        
        button_frame = customtkinter.CTkFrame(self.info_window, corner_radius=10)
        button_frame.grid(row=1, column=0, pady=(5, 10), padx=20, sticky="nsew")
        button_frame.grid_columnconfigure((0,1), weight=1) 

        # Load social media icons
        try:
            telegram_icon = customtkinter.CTkImage(Image.open("images/Telegram_icon.png"), size=(30, 30))
            whatsapp_icon = customtkinter.CTkImage(Image.open("images/WhatsApp_icon.png"), size=(30, 30))
            facebook_icon_btn = customtkinter.CTkImage(Image.open("images/Facebook_icon.png"), size=(30, 30))
            instagram_icon_btn = customtkinter.CTkImage(Image.open("images/Instegram_icon.png"), size=(30, 30))
            linkedin_icon_btn = customtkinter.CTkImage(Image.open("images/LinkedIn_icon.png"),size=(30, 30))
            about_icon = customtkinter.CTkImage(Image.open("images/Information_icon.png"), size=(30, 30))
        except FileNotFoundError:
            telegram_icon = whatsapp_icon = facebook_icon_btn = instagram_icon_btn = about_icon = None

        # Social Media Buttons
        btn_font = customtkinter.CTkFont(size=13, weight="bold")
        btn_height = 35

        telegram_button = customtkinter.CTkButton(button_frame, text="Telegram", image=telegram_icon, compound="left",
                                                    command=lambda: self.open_url(self.u_tele),
                                                    font=btn_font, height=btn_height)
        telegram_button.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

        whatsapp_button = customtkinter.CTkButton(button_frame, text="WhatsApp", image=whatsapp_icon, compound="left",
                                                    command=lambda: self.open_url(self.my_whatsapp),
                                                    font=btn_font, height=btn_height)
        whatsapp_button.grid(row=0, column=1, pady=10, padx=10, sticky="ew")

        facebook_button = customtkinter.CTkButton(button_frame, text="Facebook", image=facebook_icon_btn, compound="left",
                                                    command=lambda: self.open_url(self.u_face),
                                                    font=btn_font, height=btn_height)
        facebook_button.grid(row=1, column=0, pady=10, padx=10, sticky="ew")

        instagram_button = customtkinter.CTkButton(button_frame, text="Instagram", image=instagram_icon_btn, compound="left",
                                                    command=lambda: self.open_url(self.my_ins),
                                                    font=btn_font, height=btn_height)
        instagram_button.grid(row=1, column=1, pady=10, padx=10, sticky="ew")
        
        linkedin_button = customtkinter.CTkButton(button_frame, text="LinkedIn", image=linkedin_icon_btn, compound="left",
                                                    command=lambda: self.open_url(self.my_linkedin),
                                                    font=btn_font, height=btn_height)
        linkedin_button.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="ew")


        # About Application Button
        about_app_button = customtkinter.CTkButton(button_frame, text="About Application", image=about_icon, compound="left",
                                                command=self.show_about_app_details,
                                                font=btn_font, height=btn_height)
        about_app_button.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        # About Developer Button
        about_developer_button = customtkinter.CTkButton(button_frame, text="About Developer", image=about_icon, compound="left",
                                                command=self.show_about_developer,
                                                font=btn_font, height=btn_height)
        about_developer_button.grid(row=4, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
        
        # Close
        self.close_button = customtkinter.CTkButton(button_frame, text="Close",command=self.info_window.destroy, width=100, height=30,fg_color="red", hover_color="darkred")
        self.close_button.grid(row=5, column=0, columnspan=2, pady=10, padx=10)

    
        
        self.info_window.grab_set() # Make the info window modal
        self.master.wait_window(self.info_window)
        
if __name__ == "__main__":
    app = customtkinter.CTk()
    AnyLinkDownloaderApp(app)
    app.mainloop()  