import cv2
import torch
import numpy as np
import torchvision.transforms


def torch_tensor2mat(img):
    if len(img.size()) == 4:
        img = torch.squeeze(img, 0)  # 删除第0维

    img = torch.permute(img, (1, 2, 0))  # 交换维度
    img = img.detach().numpy()
    img = img * 255
    img = np.uint8(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)#rgb 转 bgr,否则后续opencv操作会报错
    return img

if __name__ == '__main__':
    img = 128 * np.ones((100,200,3), dtype=np.uint8)
    img = torchvision.transforms.ToTensor()(img)

    # Work().torch_tensor2mat(img)

    Work.torch_tensor2mat(img)
