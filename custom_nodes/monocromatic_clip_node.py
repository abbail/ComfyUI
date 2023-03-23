import torch
import numpy as np
from PIL import Image, ImageOps

class MonochromaticClip:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
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

    def monochromatic_clip(self, image, threshold):
        image = 255. * image[0].cpu().numpy()
        image = Image.fromarray(np.clip(image, 0, 255).astype(np.uint8))
        image = ImageOps.grayscale(image)
        image = image.convert("L").point(lambda x: 255 if x > threshold else 0, mode="1")
        image = image.convert("RGB")
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]
        
        return (image,)

NODE_CLASS_MAPPINGS = {
    "MonochromaticClip": MonochromaticClip
}