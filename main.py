import json
import os
import subprocess
import argparse


def start_stream(prod: bool) -> None:
    filename = 'settings.prod.json' if prod is True else 'settings.json'
    with open(filename, 'r') as js:
        settings = json.load(js)

        mona_proc = None
        try:
            mona_proc = subprocess.Popen([r'.\MonaServer\MonaServer.exe'], cwd=r'.\MonaServer')
            input("Started Mona. Please start your stream, then hit enter to start the multi stream.")

            twitch = f'[f=flv]{(settings["twitch_server"])}/{settings["twitch_streamkey"]}'
            yt = f'[f=flv]{(settings["youtube_server"])}/{settings["youtube_streamkey"]}'
            command = f'-i rtmp://localhost:1935/live/stream -c:v copy -c:a copy -map 0 -f tee "{twitch}|{yt}"'
            os.system(rf'.\ffmpeg\bin\ffmpeg.exe {command}')

            input("Press Enter to kill processes...")
            mona_proc.kill()
        except Exception as err:
            if mona_proc is not None:
                mona_proc.kill()
            print("Exception occured: ", err)


def main():
    parser = argparse.ArgumentParser(prog="MultiStream",
                                     description="Python script to stream to multiple sites simultaneously")
    parser.add_argument('-p', '--prod', action='store_true')
    args = parser.parse_args()

    start_stream(args.prod)


if __name__ == '__main__':
    main()
