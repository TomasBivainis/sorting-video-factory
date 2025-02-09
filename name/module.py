from PIL import Image, ImageDraw
import random
import os
from numpy import asarray
from moviepy.editor import *
import sys
import subprocess

video_width = 1280
video_height = 720
header_height = 40
length = 100

column_width = video_width / length
column_height = ((video_height - header_height) / length)

fps = 50

clips = []

colors = {
  "white": (255, 255, 255),
  "red": (255, 0, 0),
  "green": (0, 255, 0),
  "black": (0, 0, 0),
}

column_colors = []
default_colors = []

video_dir = './video/'

def make_frame(nums):
  global video_height
  global video_width
  global column_width
  global column_height
  global column_colors
  
  img = Image.new('RGB', (video_width, video_height))

  draw = ImageDraw.Draw(img)

  for i in range(len(nums)):
    draw.rectangle([(i * column_width, video_height - nums[i] * column_height), ((i + 1) * column_width, video_height)], column_colors[i], outline=colors["black"])

  return asarray(img)

def add_clip(nums):
  clips.append(make_frame(nums))

def compare(a, b, nums):
  assign_color(a, "green")
  assign_color(b, "red")
  return nums[a] > nums[b]

def swap(a, b, nums):
  tmp = nums[a]
  nums[a] = nums[b]
  nums[b] = tmp
  add_clip(nums)
  reset_colors()
  return nums

def assign_color(x, color):
  global column_colors
  global colors
  
  column_colors[x] = colors[color]

def generate_numbers():
  global default_colors
  
  nums = []
  for i in range(1, length + 1):
    nums.append(i)
    default_colors.append(colors["white"])

  random.shuffle(nums)

  return nums

def go_through(nums):
  for i in range(len(nums)):
    assign_color(i, "red")
    add_clip(nums)
    assign_color(i, "green")

  reset_colors()
  
  add_clip(nums)

def reset_colors():
  global column_colors
  global default_colors
  column_colors = default_colors.copy()

def render(algorithm):
  nums = generate_numbers()
  reset_colors()
  
  add_clip(nums)
  
  algorithm(nums)
  
  go_through(nums)

  if not os.path.exists(video_dir):
    os.mkdir(video_dir)

  final_clip = ImageSequenceClip(clips, fps=fps)

  final_clip.write_videofile(video_dir + 'movie.mp4', fps=fps)
  

def get_ffmpeg_path():
    system = sys.platform
    
    directories = __file__.split('/')
    
    project_directory = ''
    
    for i in range(1, len(directories) - 1):
      project_directory += '/' + directories[i]
    
    if system == "linux" or system == "linux2":
        return os.path.join(os.path.dirname(project_directory), "ffmpeg", "linux", "bin", "ffmpeg")
    elif system == "darwin":
        return os.path.join(os.path.dirname(project_directory), "ffmpeg", "macos", "ffmpeg")
    elif system == "win32":
        return os.path.join(os.path.dirname(project_directory), "ffmpeg", "windows", "bin", "ffmpeg.exe")
    else:
        raise EnvironmentError("Unsupported platform!")
      
def run_ffmpeg():
    ffmpeg_path = get_ffmpeg_path()
    print(ffmpeg_path)
    try:
        subprocess.run([ffmpeg_path, '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # print("FFmpeg is ready to use!")
    except FileNotFoundError:
        print(f"Could not find FFmpeg at {ffmpeg_path}")
        raise FileNotFoundError("Could not find FFmpeg")

run_ffmpeg()
      
