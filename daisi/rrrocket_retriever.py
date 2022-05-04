import os
import requests
import tarfile
import tempfile


def get_latest_rrrocket_release():
    release_info = requests.get('https://api.github.com/repos/nickbabcock/rrrocket/releases/latest')

    if release_info.status_code != 200:
        return 'Failed to retrieve from github.'

    release_info = release_info.json()

    for asset in release_info['assets']:
        if 'linux' in asset['browser_download_url'].lower():
            file_data = requests.get(asset['browser_download_url'])

            if file_data.status_code != 200:
                return 'Failed to retrieve file contents.'

            out_file_path = f'{tempfile.gettempdir()}/{asset["name"]}'

            with open(out_file_path, 'wb') as out_file:
                out_file.write(file_data.content)

            with tarfile.open(out_file_path) as tarball:
                file_names = tarball.getnames()
                output_file = file_names[-1]
                output_dir = file_names[0]
                tarball.extractall('.')

            os.remove(out_file_path)

            if os.path.exists(f'{tempfile.gettempdir()}/rrrocket'):
                os.remove(f'{tempfile.gettempdir()}/rrrocket')

            os.rename(output_file, f'{tempfile.gettempdir()}/rrrocket')
            os.rmdir(output_dir)

            return f'{tempfile.gettempdir()}/rrrocket'


if __name__ == '__main__':
    print(get_latest_rrrocket_release())
