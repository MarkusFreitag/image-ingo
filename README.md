# image-ingo
Python3 script for sorting images.

The script looks recursively through the `SOURCEPATH`, searching for image files. Then it generates a new path/filename for each of them.
The complete destination path looks like `DESTINATIONPATH/FILETYPE/TOPIC/PHOTOGRAPHER/`, while the filename is generated using the timestamp and an ID, incremented in the folder. The ID is only used to have several images, taken at the same time.

## Installation
```sh
sudo pip3 install git+https://github.com/MarkusFreitag/image-ingo.git
```

## Usage
```
Usage: image-ingo [OPTIONS] SOURCEPATH DESTINATIONPATH

Options:
  -t, --topic TEXT         Specify the topic of source images.  [required]
  -p, --photographer TEXT  Photographer that took the images.
  --no-preview             Disable the preview for destination files.
  --no-progress            Disable the progress bar while copying files.
  -h, --help               Show this message and exit.
```
