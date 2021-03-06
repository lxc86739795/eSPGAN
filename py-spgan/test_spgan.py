from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import models.models_spgan as models
import torch
import torch._utils
import torch.nn as nn
from torch.autograd import Variable
import torchvision
import torchvision.datasets as dsets
import torchvision.transforms as transforms
import torchvision
import utils.utils as utils

"""params"""
lr = 0.0002
crop_size_w = 128
crop_size_h = 256
batch_size = 24

Ga = models.Generator()
Gb = models.Generator()
transform = transforms.Compose([
    transforms.Resize((crop_size_h, crop_size_w)),
 #   transforms.RandomCrop(crop_size),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])
a_test_dir = '../Cycledata/market2duke/link_testA'
b_test_dir = '../Cycledata/market2duke/link_testB'
a_test_data = dsets.ImageFolder(a_test_dir, transform=transform)
b_test_data = dsets.ImageFolder(b_test_dir, transform=transform)
a_test_loader = torch.utils.data.DataLoader(a_test_data, batch_size=batch_size, num_workers=0)
b_test_loader = torch.utils.data.DataLoader(b_test_data, batch_size=batch_size, num_workers=0)

Ga.load_state_dict(torch.load('./checkpoints/spgan_sgd/Epoch_(7).ckpt', map_location=lambda storage, loc: storage)['Ga'])
Gb.load_state_dict(torch.load('./checkpoints/spgan_sgd/Epoch_(7).ckpt', map_location=lambda storage, loc: storage)['Gb'])
dirpatha, a, filenamea = os.walk('../Cycledata/market2duke/link_testA/0').next()
filenamea.sort()
dirpathb, b, filenameb = os.walk('../Cycledata/market2duke/link_testB/0').next()
filenameb.sort()

save_dir_a = './market/bounding_box_train_spgan_sgd/'
save_dir_b = './duke/bounding_box_train_spgan_sgd/'
utils.mkdir([save_dir_a, save_dir_b])

Ga = Ga.cuda()
Gb = Gb.cuda()

i = 0

for  a_test in (a_test_loader):
    Gb.eval()
    a_test = a_test[0]
    a_test = Variable(a_test.cuda(), volatile=True)
    a_out = Gb(a_test)
    for j in range(batch_size):
        torchvision.utils.save_image((a_out.data[j] + 1) / 2.0, save_dir_a + filenamea[i+j], padding=0)
    i+=batch_size
    if i%128 ==0: print(i)

i = 0
for  b_test in (b_test_loader):
    Ga.eval()
    b_test = b_test[0]
    b_test = Variable(b_test.cuda(), volatile=True)
    b_out = Ga(b_test)
    for j in range(batch_size):
    
        torchvision.utils.save_image((b_out.data[j] + 1) / 2.0, save_dir_b + filenameb[i+j], padding=0)
    i+=batch_size
    if i%128 ==0: print(i)




