import torch
import numpy as np
from PIL import Image, ImageOps

class ImageToMask:
    channels = ["red", "green", "blue", "black only", "white only", "greyscale", "no mask", "mask all"]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "channel": (s.channels, {"default": s.channels[0]}),
            },
        }

    RETURN_TYPES = ("MASK",)
    FUNCTION = "image_to_mask"
    
    OUTPUT_NODE = True
    CATEGORY = "image"

    def image_to_mask(self, image, channel):
        raw_image = 255. * image[0].cpu().numpy()
        i = Image.fromarray(np.clip(raw_image, 0, 255).astype(np.uint8))
        mask = None
        # r,g,b
        if channel in ["red", "green", "blue"]:
            c = channel[0].upper()
            mask = np.array(i.getchannel(c)).astype(np.float32) / 255.0
            mask = torch.from_numpy(mask)
        # black or white
        elif channel == "black only" or channel == "white only":
            if channel == "black only":
                filter = lambda x: 0 if x > 0 else 1
            elif channel == "white only":
                filter = lambda x: 1 if x == 255 else 0
            mask = np.array(i.convert("L").point(filter, mode="1")).astype(np.float32)
            mask = torch.from_numpy(mask)
        # greyscale
        elif channel == "greyscale":
            print(ImageOps.grayscale(i).getbands())
            mask = np.array(ImageOps.grayscale(i).getchannel("L")).astype(np.float32) / 255.0
            mask = 1. - torch.from_numpy(mask)
        # mask everything
        elif channel == "mask all":
            mask = torch.ones((64,64), dtype=torch.float32, device="cpu")
        # mask nothing
        else:
            mask = torch.zeros((64,64), dtype=torch.float32, device="cpu")
        return (mask,)

NODE_CLASS_MAPPINGS = {
    "ImageToMask": ImageToMask
}