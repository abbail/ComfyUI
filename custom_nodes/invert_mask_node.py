import torch

class InvertMask:
    channels = ["red", "green", "blue", "greyscale", "black only", "white only", "mask everything", "mask nothing"]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mask": ("MASK",)
            }
        }

    RETURN_TYPES = ("MASK",)
    FUNCTION = "invert_mask"
    
    CATEGORY = "image"

    def invert_mask(self, mask):
        ones = torch.ones(mask.shape, dtype=torch.float32, device="cpu")
        mask = torch.sub(ones, mask)
        return (mask,)

NODE_CLASS_MAPPINGS = {
    "InvertMask": InvertMask
}