import folder_paths
import comfy.sd

class ImageToDepth:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "midas_ckpt_name": (folder_paths.get_filename_list("checkpoints"), {"default": "512-depth-ema.safetensors"})
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "image_to_depth"

    CATEGORY = "image"

    def image_to_depth(self, image, midas_ckpt_name):
        ckpt = folder_paths.get_full_path("checkpoints", midas_ckpt_name)
        print(ckpt)
        parameters = comfy.sd.load_torch_file(ckpt)
        if "optimizer" in parameters:
            parameters = parameters["model"]
        print(sd)

        return (image,)

NODE_CLASS_MAPPINGS = {
    "ImageToDepth": ImageToDepth
}