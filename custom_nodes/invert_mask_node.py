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
        mask = ~mask
        return (mask,)

NODE_CLASS_MAPPINGS = {
    "InvertMask": InvertMask
}