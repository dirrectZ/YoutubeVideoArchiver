import datetime
import os.path
import tkinter
from tkinter import filedialog
import pytube
import scrapetube


class App(tkinter.Tk):
	def __init__(self):
		super().__init__()
		self.title = "YoutubeVideoArchiver"
		self.geometry("480x240")
		self.main_window = MainFrame()
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		self.main_window.grid(row=0, column=0, sticky="nsew")
		

class MainFrame(tkinter.Frame):
	def __init__(self, **kwargs):
		super().__init__()
		self.channel_link = tkinter.StringVar()
		self.location = tkinter.StringVar()
		
		self.columnconfigure(0, weight=1)
		
		# LINK
		self.frame_channel_link = tkinter.LabelFrame(self, text="Channel Link")
		self.frame_channel_link.grid(row=0, column=0, sticky="nsew", padx=(30, 30), pady=(15, 5))
		self.frame_channel_link.columnconfigure(0, weight=1)
		
		self.entry_channel_link = tkinter.Entry(self.frame_channel_link, textvariable=self.channel_link, font=("", 18))
		self.entry_channel_link.grid(row=0, column=0, sticky="nsew")

		# LOCATION
		self.frame_location = tkinter.LabelFrame(self, text="Location")
		self.frame_location.grid(row=1, column=0, sticky="nsew", padx=(30, 30), pady=(15, 5))
		self.frame_location.columnconfigure(0, weight=1)
		
		self.entry_location = tkinter.Entry(self.frame_location, textvariable=self.location, font=("", 18))
		self.entry_location.grid(row=0, column=0, sticky="nsew")
		# self.entry_location.bind("<FocusIn>", self.location_focus)
		self.location_button = tkinter.Button(self.frame_location, command=self.location_change, bitmap='questhead')
		self.location_button.grid(row=0, column=1)
		
		self.start_button = tkinter.Button(self, text="START", command=self.download_videos, font=("", 20))
		self.start_button.grid(row=2, column=0, pady=(20, 0))
		
	def location_change(self):
		new_dir = filedialog.askdirectory(initialdir=self.location.get())
		if new_dir:
			self.location.set(new_dir)
			
	def download_videos(self):
		
		channel_url = self.channel_link.get()
		title = str(datetime.datetime.utcnow())
		output_dir = os.path.join(self.location.get(), title)

		videos = scrapetube.get_channel(channel_url=channel_url)
		if output_dir:
			try:
				for v in videos:
					link = f"https://www.youtube.com/watch?v={v['videoId']}"
					yt_video = pytube.YouTube(link)
					stream = yt_video.streams.get_by_itag(22)
					stream.download(output_path=output_dir, filename=f"{yt_video.title}.mp4")
			except:
				pass
			
		
if __name__ == "__main__":
	app = App()
	app.mainloop()
	