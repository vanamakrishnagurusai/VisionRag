from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration


class ImageCaptioner:

    def __init__(
        self,
        model_name="Salesforce/blip-image-captioning-base"
    ):

        print(
            f"Loading captioning model: {model_name}"
        )

        self.processor = BlipProcessor.from_pretrained(
            model_name
        )

        self.model = BlipForConditionalGeneration.from_pretrained(
            model_name
        )

    def generate_caption(self, image_path):

        image = Image.open(
            image_path
        ).convert("RGB")

        inputs = self.processor(
            images=image,
            return_tensors="pt"
        )

        output = self.model.generate(
            **inputs,
            max_new_tokens=50
        )

        caption = self.processor.decode(
            output[0],
            skip_special_tokens=True
        )

        return caption