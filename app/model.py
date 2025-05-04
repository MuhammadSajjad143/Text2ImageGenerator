from diffusers import StableDiffusionPipeline
import torch

class Text2ImageModel:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = StableDiffusionPipeline.from_pretrained(
            "CompVis/stable-diffusion-v1-4",
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            safety_checker=None,  # Disable safety checker for production
            resume_download=True
        ).to(self.device)

    def generate(self, prompt):
        try:
            with torch.no_grad():
                image = self.pipe(prompt, num_inference_steps=30).images[0]
            return image
        except Exception as e:
            raise Exception(f"Image generation failed: {str(e)}")