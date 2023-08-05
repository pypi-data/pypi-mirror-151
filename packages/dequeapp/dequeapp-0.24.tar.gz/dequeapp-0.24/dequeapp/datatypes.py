from PIL import Image
import pickle
import json
import time
import util
import numpy as np

class BoundingBox2D():
    def __init__(self):
        self.coordinates = {}
        self.domain = None
        self.scores = {}
        self.caption = ""
        self.labels = {}

class DequeImage:


    def __init__(self, data, bounding_boxes=None, mode=None):

        if isinstance(data, Image):
            self._image = data
            print("I am PIL image")
        elif util.is_type_torch_tensor(util.get_full_typename(data)):
            vis_util = util.get_module(
                "torchvision.utils", "torchvision is required to render images"
            )
            if hasattr(data, "requires_grad") and data.requires_grad:
                data = data.detach()
            data = vis_util.make_grid(data, normalize=True)
            self._image = Image.fromarray(
                data.mul(255).clamp(0, 255).byte().permute(1, 2, 0).cpu().numpy()
            )
            print("I used to be tensor image")
        else:
            if hasattr(data, "numpy"):  # TF data eager tensors
                data = data.numpy()
            if data.ndim > 2:
                data = data.squeeze()  # get rid of trivial dimensions as a convenience
            self._image = Image.fromarray(
                self.to_uint8(data), mode=mode or self.guess_mode(data)
            )
            print("I used to be numpy image")


        self.type = "Deque.Image"

    def guess_mode(self, data: "np.ndarray") -> str:
        """
        Guess what type of image the np.array is representing
        """
        # TODO: do we want to support dimensions being at the beginning of the array?
        if data.ndim == 2:
            return "L"
        elif data.shape[-1] == 3:
            return "RGB"
        elif data.shape[-1] == 4:
            return "RGBA"
        else:
            raise ValueError(
                "Un-supported shape for image conversion %s" % list(data.shape)
            )

    @classmethod
    def to_uint8(cls, data: "np.ndarray") -> "np.ndarray":
        """
        Converts floating point image on the range [0,1] and integer images
        on the range [0,255] to uint8, clipping if necessary.
        """
        np = util.get_module(
            "numpy",
            required="Deque.Image requires numpy if not supplying PIL Images: pip install numpy",
        )


        dmin = np.min(data)
        if dmin < 0:
            data = (data - np.min(data)) / np.ptp(data)
        if np.max(data) <= 1.0:
            data = (data * 255).astype(np.int32)

        # assert issubclass(data.dtype.type, np.integer), 'Illegal image format.'
        return data.clip(0, 255).astype(np.uint8)




if __name__ == "__main__":
    with Image.open("/home/riju/Downloads/riju-pahwa.png") as im:
        im = im.tobytes()

    # Read a PIL image




    print(di.to_json(di))


