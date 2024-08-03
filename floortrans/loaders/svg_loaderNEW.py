
# hierdurch wird scaled.png nicht mehr benötigt
import cv2
import numpy as np
import torch
from torch.utils.data import Dataset
from numpy import genfromtxt
import lmdb
import pickle

class FloorplanSVGnew(Dataset):
    def __init__(self, data_folder, data_file, is_transform=True,
                 augmentations=None, img_norm=True, format='txt',
                 original_size=False, lmdb_folder='cubi_lmdb/'):
        self.img_norm = img_norm
        self.is_transform = is_transform
        self.augmentations = augmentations
        self.get_data = None
        self.original_size = original_size
        self.image_file_name = '/F1_original.png'  # Original image file
        self.lmdb_folder = lmdb_folder

        if format == 'txt':
            self.get_data = self.get_txt
        elif format == 'lmdb':
            self.lmdb = lmdb.open(data_folder + lmdb_folder, readonly=True,
                                  max_readers=8, lock=False,
                                  readahead=True, meminit=False)
            self.get_data = self.get_lmdb
            self.is_transform = False

        self.data_folder = data_folder
        self.folders = genfromtxt(data_folder + data_file, dtype='str')

    def __len__(self):
        return len(self.folders)

    def __getitem__(self, index):
        sample = self.get_data(index)

        if self.augmentations is not None:
            sample = self.augmentations(sample)
            
        if self.is_transform:
            sample = self.transform(sample)

        return sample

    def get_txt(self, index):
        fplan = cv2.imread(self.data_folder + self.folders[index] + self.image_file_name)
        fplan = cv2.cvtColor(fplan, cv2.COLOR_BGR2RGB)
        
        # Resize image to a fixed size if original_size is False
        if not self.original_size:
            fplan = cv2.resize(fplan, (256, 256))

        height, width, nchannel = fplan.shape
        fplan = np.moveaxis(fplan, -1, 0)

        img = torch.tensor(fplan.astype(np.float32))

        sample = {'image': img, 'folder': self.folders[index]}

        return sample

    def get_lmdb(self, index):
        key = self.folders[index].encode()
        with self.lmdb.begin(write=False) as f:
            data = f.get(key)

        sample = pickle.loads(data)
        return sample

    def transform(self, sample):
        fplan = sample['image']
        fplan = 2 * (fplan / 255.0) - 1
        sample['image'] = fplan

        return sample

