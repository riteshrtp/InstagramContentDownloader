import argparse
import os
import requests
import time
import urllib.request
from colorama import init, deinit
from termcolor import cprint #Prints `text` in passed `color`
import tkinter as tk
from functools import partial

def windowsInterface():
	print("WINDOWS Interface::\nInsta UserID: %s\ndownload location %s" % (e1.get(), e2.get()))

def image_downloader(edge, images_path):
	display_url = edge['node']['display_url']
	file_name = edge['node']['taken_at_timestamp']
	download_path = f"{images_path}\\{file_name}.jpg"
	if not os.path.exists(download_path):
		cprint(f"Downloading {str(file_name)}.jpg...........", "yellow")
		urllib.request.urlretrieve(display_url, download_path)
		cprint(f"{file_name}.jpg downloaded.\n", "green")
	else:
		cprint(f"{file_name}.jpg has been downloaded already.\n", "green")

def video_downloader(shortcode, videos_path):
    """ Downloads videos """
    videos = requests.get(f"https://www.instagram.com/p/{shortcode}/?__a=1")
    video_url = videos.json()['graphql']['shortcode_media']['video_url']
    file_name = videos.json()['graphql']['shortcode_media']['taken_at_timestamp']
    download_path = f"{videos_path}\\{file_name}.mp4"
    if not os.path.exists(download_path):
        cprint(f"Downloading {file_name}.mp4...........", "yellow")
        urllib.request.urlretrieve(video_url, download_path)
        cprint(f"{file_name}.mp4 downloaded.\n", "green")
    else:
        cprint(f"{file_name}.mp4 has been downloaded already.\n", "green")

def sidecar_downloader(shortcode, images_path, videos_path):
    """ Downloads images and videos from posts containing more than one pictures or videos """
    r = requests.get(f"https://www.instagram.com/p/{shortcode}/?__a=1")
    num = 1
    for edge in r.json()['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']:
        is_video = edge['node']['is_video']
        if not is_video:
            display_url = edge['node']['display_url']
            file_name = r.json()['graphql']['shortcode_media']['taken_at_timestamp']
            download_path = f"{images_path}\\{file_name}_{num}.jpg"
            if not os.path.exists(download_path):
                cprint(f"Downloading {file_name}_{num}.jpg...........", "yellow")
                urllib.request.urlretrieve(display_url, download_path)
                cprint(f"{file_name}_{num}.jpg downloaded.\n", "green")
            else:
                cprint(f"{file_name}_{num}.jpg has been downloaded already.\n", "green")
        else:
            video_url = edge['node']['video_url']
            file_name = r.json()['graphql']['shortcode_media']['taken_at_timestamp']
            download_path = f"{videos_path}\\{file_name}_{num}.mp4"
            if not os.path.exists(download_path):
                cprint(f"Downloading {file_name}_{num}.mp4...........", "yellow")
                urllib.request.urlretrieve(video_url, download_path)
                cprint(f"{file_name}_{num}.mp4 downloaded.\n", "green")
            else:
                cprint(f"{file_name}_{num}.mp4 has been downloaded already.\n", "green")
        num += 1

def mainFun(interfaceUserName, interfacePath):
    account_json_info = "https://www.instagram.com/"+interfaceUserName+"/?__a=1"
    path=""
    path += "\\"+interfaceUserName+""
    master.quit()
    print("Insta UserID: %s\ndownload location %s" % (interfaceUserName, interfacePath))
    r=requests.get(account_json_info)
    user_id = r.json()['graphql']['user']['id']
    end_cursor = ''
    next_page = True
    images_path = f"{path}\\Images"
    videos_path = f"{path}\\Videos"
    if not os.path.exists(path):
        os.makedirs(path)
        if not os.path.exists(images_path):
            os.makedirs(images_path)
        if not os.path.exists(videos_path):
            os.makedirs(videos_path)
        cprint("User Folder Created!\n", "magenta")
    else:
        cprint("User Folder Has Been Created Already!\n", "magenta")

    while next_page:
        r = requests.get('https://www.instagram.com/graphql/query/',
                params={
                    'query_id': '17880160963012870',
                    'id': user_id,
                    'first': 12,
                    'after': end_cursor
                }
            )
        graphql = r.json()['data']
        for edge in graphql['user']['edge_owner_to_timeline_media']['edges']:
            __typename = edge['node']['__typename']
            if __typename == 'GraphImage':
                image_downloader(edge, images_path)
            elif __typename == 'GraphVideo':
                shortcode = edge['node']['shortcode']
                video_downloader(shortcode, videos_path)
            elif __typename == 'GraphSidecar':
                shortcode = edge['node']['shortcode']
                sidecar_downloader(shortcode, images_path, videos_path)

        end_cursor = graphql['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        next_page = graphql['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
        time.sleep(10)
    deinit()

def call_result(t1, t2):
    interfaceUserName = (t1.get())
    print(interfaceUserName)
    interfacePath = (t2.get())
    master.quit()
    if interfacePath=='':
        interfacePath=os.getcwd()
    print("MAC Interface::\nInsta UserID: %s\nDownload location: %s" % (interfaceUserName, interfacePath))
    if interfaceUserName=='':
        cprint("~~~~~~~~~~~~~~~~~~~~RUN AGAIN AND PLEASE ENTER USERNAME~~~~~~~~~~~~~~~~~~","red")
        quit()
    
    master.quit()
    mainFun(interfaceUserName,interfacePath)

if __name__ == '__main__':
    print('\n\n')
    #init(autoreset=True)
    cprint('Instagram Media Downloader'.center(os.get_terminal_size().columns, '-'), "cyan")
    #deinit()
    master = tk.Tk()
    #if(os.name=='posix'):	
    text1 = tk.StringVar()
    text2 = tk.StringVar()
    tk.Label(master,text="Instagram UserName ").grid(row=0)
    tk.Label(master,text="Download Location ").grid(row=1)
    e1 = tk.Entry(master,textvariable=text1).grid(row=0, column=1)
    e2 = tk.Entry(master,textvariable=text2).grid(row=1, column=1)
    call_result = partial(call_result, text1, text2)  
    tk.Button(master,text='Quit',command=master.quit).grid(row=3,column=0,sticky=tk.W,pady=4)
    tk.Button(master,text='downloaded', command=call_result).grid(row=3,column=1,sticky=tk.W,pady=4)
    tk.mainloop()
    #elif(os.name=='nt'):
        #windowsInterface()



