import torch
import numpy as np
from PIL import Image, ImageOps

class MonochromaticClip:
    channels = ["red", "green", "blue", "greyscale"]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "channel": (s.channels, {"default": "greyscale"}),
                "threshold": ("INT", {
                    "default": 0, 
                    "min": 0,
                    "max": 255,
                    "step": 1
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "monochromatic_clip"

    CATEGORY = "image"

    def monochromatic_clip(self, image, channel, threshold):
        image = 255. * image[0].cpu().numpy()
        image = Image.fromarray(np.clip(image, 0, 255).astype(np.uint8))
        c = channel[0].upper()
        if channel in ["red", "green", "blue"] and c in image.getbands():
            image = image.getchannel(c)
        image = ImageOps.grayscale(image)
        image = image.convert("L").point(lambda x: 255 if x > threshold else 0, mode="1")
        image = image.convert("RGB")
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]
        
        return (image,)

NODE_CLASS_MAPPINGS = {
    "MonochromaticClip": MonochromaticClip
}