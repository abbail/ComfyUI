import torch
import numpy as np
from PIL import Image, ImageOps    


class InvertImage:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "invert_image"

    CATEGORY = "image"

    def invert_image(self, image):
        image = 255. * image[0].cpu().numpy()
        image = Image.fromarray(np.clip(image, 0, 255).astype(np.uint8))
        image = ImageOps.invert(image)
        image = image.convert("RGB")
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]
        
        return (image,)

NODE_CLASS_MAPPINGS = {
    "InvertImage": InvertImage
}