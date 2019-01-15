import google_images_download
import ssl

from google_images_download import google_images_download


def main():
    ssl._create_default_https_context = ssl._create_unverified_context
    response = google_images_download.googleimagesdownload()

    # download by keyword
    arguments = {'keywords': 'kermit', 'limit': 100, 'output_directory': 'data/google-images'}
    paths = response.download(arguments)
    print(paths)


if __name__ == '__main__':
    main()
