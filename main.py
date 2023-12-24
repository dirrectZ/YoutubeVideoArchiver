import functools
import json
import os.path
import tkinter
from tkinter import filedialog
import pytube
import scrapetube
import unidecode


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
	
		self.errors = []
		self.naming_dict = {}
		
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
		self.location_button = tkinter.Button(self.frame_location, command=self.location_change, bitmap='questhead')
		self.location_button.grid(row=0, column=1)
		
		self.start_button = tkinter.Button(self, text="START", command=self.start_downloading, font=("", 20))
		self.start_button.grid(row=2, column=0, pady=(20, 0))
		
	def location_change(self):
		new_dir = filedialog.askdirectory(initialdir=self.location.get())
		if new_dir:
			self.location.set(new_dir)
			
	def start_downloading(self):
		
		channel_url = self.channel_link.get()
		output_dir = self.location.get()
		self.video_number = 0
		self.num_of_videos = 0

		videos = scrapetube.get_channel(channel_url=channel_url)
		if output_dir:
			
			for v in videos:
				v_to_download = functools.partial(self.download_video, v, output_dir)
				self.after_idle(v_to_download)
				self.video_number += 1
				
			self.write_files(output_dir)
			
	def download_video(self, video, location):
		link = f"https://www.youtube.com/watch?v={video['videoId']}"
		try:
			yt_video = pytube.YouTube(link)
			video_title = yt_video.title
			title = self.legal_title(video_title)
			
			self.naming_dict[video_title] = title
			
			date = yt_video.publish_date
			string_date = str(date).split()[0]
			
			stream = yt_video.streams.get_by_itag(22)
			video_name = f"{title}_{string_date}.mp4"
			video_location = os.path.join(location, video_name)
			self.video_number += 1
			
			if not os.path.exists(video_location):
				stream.download(output_path=location, filename=video_name)
				
			if self.video_number % 50 == 0:
				self.write_files(location)
				
			if self.video_number == self.num_of_videos:
				self.write_files(location)
				
		except:
			self.errors.append(link)
			self.write_files(location)
			
	def write_files(self, location):
		with open(os.path.join(location, "errors.txt"), "w") as errors_file:
			for e in self.errors:
				print(e, file=errors_file)
				
		with open(os.path.join(location, "naming.json"), "w") as naming_json:
			json.dump(self.naming_dict, naming_json)
	
	@staticmethod
	def legal_title(title):
		title = unidecode.unidecode(title)
		ILLEGAL_CHARACTERS = r'<>:"/\|?*'
		
		new_title = ""
		for c in title:
			if c not in ILLEGAL_CHARACTERS:
				new_title += c
				
		return new_title
		
		
if __name__ == "__main__":
	app = App()
	app.mainloop()
	