import json
import requests
import random
from dhooks import Webhook, File
from collections import Counter
import os
from pprint import pprint
from PIL import Image, ImageFont, ImageDraw, ImageSequence
import time
import numpy as np
from moviepy.editor import ImageClip, VideoFileClip, AudioFileClip, CompositeVideoClip
import instagrapi
from pro_secrets import *

#Login to our instagram account
client = instagrapi.Client()
try:
    client.login(username=insta_credentials["username"], password=insta_credentials["password"])
except:
    pass

# This functionw will generate captions for our videos

def caption():
    listoflines = ['Follow for more such thoughts!🤯', "What's your craziest shower thought? 🚿", 'Drop your wildest thoughts below! 💭', 'Did you know? 😲'," Must've snapped your mind in half. 🧠","Me: I don't overthink. Also me:", 'Have you ever thought? 🤯']
    line = random.choice(listoflines)
    finalstring = f"""{line}
    -
    -
    -
    -
    -
    #showerthoughts #deepthoughts #randomthoughts #random #shower #deep #quotes #memes #funny #relatable #viral #fyp #trending
    """
    return finalstring

# Pull function to pull content from r/showerthoughts subreddit

def pull():
    url = "https://www.reddit.com/r/showerthoughts/hot.json?t=week&limit=6"


    client_id = reddit_credentials["client_id"]
    secret_key = reddit_credentials["secret_key"]

    auth = requests.auth.HTTPBasicAuth(client_id, secret_key)

    data = {
        'grant_type': "password",
        'username': reddit_credentials["username"],
        'password': reddit_credentials["password"]
    }

    header = {
        'User-Agent' : "justabotman"
    }

    output = requests.get(url, auth=auth, data=data, headers=header)

    if output.ok:
        data = output.json()
        with open('showerthoughts.json', 'w') as file:
            data = data['data']['children']
            json.dump(data, file)

    else:
        pprint(output.text)
        print(f"error [{output.status_code}]")

print('#################################################################################################')

# This function is to choose a random showerthought from the showerthoughts.json file and then save it without the random choosen showerthought

def generate_thought():
    with open('showerthoughts.json', 'r') as f:
        try:
            data = json.load(f)
        except:
            data = []

    pprint(data)

    ogdata = []
    if len(data) >= 2:
        ogdata = random.sample(data, 1)
    else:
        pull()
        with open('showerthoughts.json', 'r') as f:
            data = json.load(f)
        ogdata = random.sample(data, 1)
    return ogdata

truth = True

# Sometimes subreddits have this post "Forging A Return to Productive Conversation: An Open Letter To Reddit" so the while loop makes sure that such post is removed 

ogdata = generate_thought()


# Initializing discord webhook
hook = Webhook(DIScord_webhook)


try:
    hook.send("Here is some cocktail from your chef! 🍹")
except:
    pass

for item in ogdata:
    item = item['data']['title']
    folder_path = 'gif'
    # List all files in the specified directory
    files = []
    for file in os.listdir(folder_path):
        files.append(f"gif/{file}")

    # Check if there are any files in the directory
    if not files:
        raise ValueError("No gifs found in the specified directory.")

    # Choose a random gif from the list
    gif_path = random.choice(files)

    gif = Image.open(gif_path)

    # Initialize a list to store the colors
    colors = []

    # Iterate through each frame in the GIF
    for frame in range(gif.n_frames):
        gif.seek(frame)
        frame_image = gif.convert('RGB')
        colors.extend(frame_image.getdata())

    # Count the frequency of each color
    color_counts = Counter(colors)

    # Get the most common color
    major_color = color_counts.most_common(1)[0][0]

    width, height = 600, 1067

    print(f"The major color in the GIF is: {major_color}")

    # Create an empty array for the image
    gradient = np.zeros((height, width, 3), dtype=np.uint8)

    for x in range(width):
            # Calculate the ratio for blending
            ratio = (x / width) ** (1/2)
            for y in range(height):
                # Decrease the intensity of white by a factor (e.g., 0.8)
                white_intensity = 1.2
                # Calculate the color for the current pixel
                red = int((major_color[0] + 80) * white_intensity * (1 - ratio) + major_color[0] * ratio)
                green = int((major_color[1] + 80) * white_intensity * (1 - ratio) + major_color[1] * ratio)
                blue = int((major_color[2] + 80) * white_intensity * (1 - ratio) + major_color[2] * ratio)
                if red > 255:
                    red = 255
                if green > 255:
                    green = 255
                if blue > 255:
                    blue = 255
                r = red
                g = green
                b = blue
                gradient[y, x] = (r, g, b)

    # Create an image from the array
    bgimage = Image.fromarray(gradient)

    bgimage.save("bgimage.png")

    def resize_and_crop_gif(input_path, output_path, target_width=474):
        with Image.open(input_path) as img:
            frames = []
            for frame in ImageSequence.Iterator(img):
                frame = frame.convert("RGBA")

                # Calculate new dimensions maintaining aspect ratio
                aspect_ratio = frame.height / frame.width
                new_width = target_width
                new_height = int(new_width * aspect_ratio)

                # Resize frame
                resized_frame = frame.resize((new_width, new_height), Image.LANCZOS)
                frames.append(resized_frame)

            # Save the frames as a new GIF
            frames[0].save(output_path, save_all=True, append_images=frames[1:], loop=0, duration=img.info['duration'])

    img = Image.open(gif_path)
    gifFrame = ImageSequence.Iterator(img)[0]
    frame = gifFrame.convert("RGBA")

    aspect_ratio = frame.height / frame.width
    new_width = 474
    gif_height = int(new_width * aspect_ratio)

    resize_and_crop_gif(gif_path, gif_path)

    "-----------------------------------------------Building the post-------------------------------------------"

    profile_pic_path = "topface.png"  # Path to profile picture
    username = "DailyThoughtDrops"
    content = item
    output_path = "twitter_post.png"

    # Dimensions
    width = 540
    space_for_image = gif_height
    profile_pic_size = 72
    padding = 34
    content_start_y = profile_pic_size + 2 * padding

    # Load profile picture and resize
    profile_pic = Image.open(profile_pic_path).resize((profile_pic_size, profile_pic_size))

    # Font settings (you might need to change the font path based on your system)
    font_path = "Roboto-Regular.ttf"  # Ensure this font is available on your system
    username_font = ImageFont.truetype(font_path, 24)
    content_font = ImageFont.truetype(font_path, 24)

    # Create an image with a white background
    img = Image.new('RGB', (width, 300), color='white')
    draw = ImageDraw.Draw(img)

    # Calculate text sizes
    username_bbox = draw.textbbox((0, 0), username, font=username_font)
    username_width = username_bbox[2] - username_bbox[0]
    username_height = username_bbox[3] - username_bbox[1]

    content_lines = []
    words = content.split()
    line = ""
    for word in words:
        test_line = f"{line} {word}".strip()
        textbox = draw.textbbox((0, 0), test_line, font=content_font)
        test_line_width = textbox[2] - textbox[0]
        if test_line_width <= width - 2 * padding:
            line = test_line
        else:
            content_lines.append(line)
            line = word
    content_lines.append(line)

    line_heights = []

    for line in content_lines:
        linetextbox = draw.textbbox((0, 0), line, font=content_font)
        line_height = linetextbox[3] - linetextbox[1]
        line_heights.append(line_height)
        line_heights.append(19)
    line_heights.remove(19)
    content_height = sum(line_heights)

    # Resize image height to fit content
    img_height = content_start_y + content_height + 2 * padding + space_for_image
    img = img.resize((width, img_height))
    draw = ImageDraw.Draw(img)

    # Paste profile picture
    img.paste(profile_pic, (padding, padding))

    # Draw username
    draw.text((padding + 13 + profile_pic_size, padding + ((profile_pic_size)/2 - username_height) - 6), username, font=username_font, fill='black')
    draw.text((padding + 13 + profile_pic_size, padding + ((profile_pic_size)/2)), f"@{username.lower()}", font=username_font, fill='gray')

    # Draw content
    current_y = content_start_y
    for line in content_lines:
        draw.text((padding, current_y), line, font=content_font, fill='black')
        linetextbox = draw.textbbox((0, 0), line, font=content_font)
        line_height = linetextbox[3] - linetextbox[1]
        current_y += line_height + 19

    # Save the image
    img.save(output_path)
    print(f"Twitter post image saved to {output_path}")

    "--------------------------------------------moviepy magic-------------------------------------------------"


    # Load the gif
    gif = VideoFileClip(gif_path)
    gif = gif.loop(duration=5)

    # Load the background image
    audio = AudioFileClip("bgmusic (1).mp3").set_duration(6)
    background_image = ImageClip("bgimage.png").set_duration(6)  # Set duration arbitrarily

    # Load the overlay image
    overlay_image = ImageClip("twitter_post.png").set_duration(6)

    # Calculate the relative y value
    topyofpost = content_start_y + content_height + padding
    topyvalue = topyofpost + ((bgimage.size[1] - img.size[1])/2)
    relyvalue = topyvalue/bgimage.size[1]

    # Calculate the relative x value
    relxvalue = ((bgimage.size[0] - 474)/2)/bgimage.size[0]

    # Resize and set the position of the GIF
    gif = gif.set_position((relxvalue, relyvalue), relative=True).set_duration(6)

    # Set the overlay image's position
    overlay_image = overlay_image.set_pos(("center", "center"))

    # Composite the final video
    final_video = CompositeVideoClip([background_image, overlay_image, gif]).set_audio(audio)

    # Write the result to a file
    final_video.write_videofile("final_video.mp4", codec="libx264", fps=30)

    try:
        hook.send(file=File("final_video.mp4"))
    except:
        pass

    captionn = caption()
    try:
        client.clip_upload('final_video.mp4', captionn)
    except Exception as e:
        hook.send(f"""Unfortunately unable to post the reel cause of:
            {e}
            """)

    time.sleep(11)