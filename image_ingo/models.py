import click
import exifread
import os
from shutil import copyfile


class File():
    def __init__(self, name, path):
        self.name = name
        self.path = path

    @property
    def ending(self):
        return self.name.split('.')[-1]

    @property
    def absolute_path(self):
        return os.path.join(self.path, self.name)


class Image():
    def __init__(self, filename, path):
        self.__set_source_file(filename, path)
        self.__destination_file = None

    def __get_source_file(self):
        return self.__source_file

    def __set_source_file(self, filename, path):
        self.__source_file = File(filename, path)

    source_file = property(__get_source_file, __set_source_file)

    @property
    def destination_file(self):
        return self.__destination_file

    @property
    def timestamp(self):
        return self.__timestamp

    @property
    def type(self):
        return self.source_file.ending

    @property
    def filename(self):
        return self.source_file.name.split('.')[0]

    def parse_exif_data(self):
        with open(self.__source_file.absolute_path, 'rb') as file_:
            tags = exifread.process_file(file_, details=False, stop_tag='DateTimeOriginal')
            self.__timestamp = str(tags['EXIF DateTimeOriginal']).replace(':', '-').replace(' ', '_')

    def show(self):
        return '{} | {} -> {}'.format(self.timestamp,
                                      self.source_file.absolute_path,
                                      self.destination_file.absolute_path)

    def create_destination_file(self, img_id, destination_path):
        dest_fname = 'IMG_{}_{}.{}'.format(self.timestamp,
                                           img_id,
                                           self.source_file.ending)
        self.__destination_file = File(dest_fname, destination_path)


class ImageList():
    def __init__(self, source_path, destination_path, topic, photograph, type_):
        self.source_path = source_path
        self.destination_path = os.path.join(destination_path, type_, topic, photograph)
        self.topic = topic
        self.photograph = photograph
        self.images = []
        self.type_ = type_
        self.__starting_img_id = 0
        if os.path.exists(self.destination_path):
            files = os.listdir(self.destination_path)
            if files:
                self.__starting_img_id = int(files[-1].split('_')[3].split('.')[0])

    def add_image(self, filename, path):
        self.images.append(Image(filename, path))

    def load(self):
        for path, subdirs, files in os.walk(self.source_path):
            for file_ in files:
                if file_.endswith(self.type_):
                    self.add_image(file_, path)
        self.images.sort(key=lambda x: x.filename)

    def process(self):
        for index, img in enumerate(self.images):
            img.parse_exif_data()
            img.create_destination_file(str(self.__starting_img_id+index+1), self.destination_path)

    def preview(self):
        return '\n'.join([img.show() for img in self.images])

    def copy_files(self, no_progress=False):
        os.makedirs(self.destination_path, exist_ok=True)
        if no_progress:
            for img in self.images:
                copyfile(img.source_file.absolute_path, img.destination_file.absolute_path)
        else:
            with click.progressbar(self.images, label='Copying images') as bar:
                for img in bar:
                    copyfile(img.source_file.absolute_path, img.destination_file.absolute_path)
