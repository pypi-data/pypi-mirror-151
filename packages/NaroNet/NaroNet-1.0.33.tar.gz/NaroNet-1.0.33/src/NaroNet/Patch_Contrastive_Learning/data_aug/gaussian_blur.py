import numpy as np
import torch
from torch import nn
from torchvision.transforms import transforms

np.random.seed(0)


class GaussianBlur(object):
    """blur a single image on CPU"""
    def __init__(self, kernel_size, in_channels):
        radias = kernel_size // 2
        kernel_size = radias * 2 + 1
        self.in_channels = in_channels
        self.blur_h = nn.Conv2d(in_channels, in_channels, kernel_size=(kernel_size, 1),
                                stride=1, padding=0, bias=False, groups=in_channels)
        self.blur_v = nn.Conv2d(in_channels, in_channels, kernel_size=(1, kernel_size),
                                stride=1, padding=0, bias=False, groups=in_channels)
        self.k = kernel_size
        self.r = radias

        self.blur = nn.Sequential(
            nn.ReflectionPad2d(radias),
            self.blur_h,
            self.blur_v
        )

        self.pil_to_tensor = transforms.ToTensor()
        self.tensor_to_pil = transforms.ToPILImage()

    def __call__(self, img):
        # img = self.pil_to_tensor(img).unsqueeze(0)

        sigma = np.random.uniform(0.1, 2.0)
        x = np.arange(-self.r, self.r + 1)
        x = np.exp(-np.power(x, 2) / (2 * sigma * sigma))
        x = x / x.sum()
        x = torch.from_numpy(x).view(1, -1).repeat(self.in_channels, 1)

        self.blur_h.weight.data.copy_(x.view(self.in_channels, 1, self.k, 1))
        self.blur_v.weight.data.copy_(x.view(self.in_channels, 1, 1, self.k))

        with torch.no_grad():
            img = self.blur(img)
            img = img.squeeze()

        return img