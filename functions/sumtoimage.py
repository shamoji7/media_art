import os
import io
import warnings
from IPython.display import display
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import matplotlib.pyplot as plt
from datetime import datetime

os.environ['STABILITY_HOST'] = 'YOUR-HOST'
os.environ['STABILITY_KEY'] = 'YOUR-API-KEY'


stability_api = client.StabilityInference(
    key=os.environ['STABILITY_KEY'], 
    verbose=True, 
    engine="stable-diffusion-v1-5", 
    # Available engines: stable-diffusion-v1 stable-diffusion-v1-5 stable-diffusion-512-v2-0 stable-diffusion-768-v2-0 stable-inpainting-v1-0 stable-inpainting-512-v2-0
    ) 

answers = stability_api.generate(
    prompt=input(),
    #seed=992446758, 
    steps=30, 
    cfg_scale=8.0,
    width=512, 
    height=512, 
    samples=1, 
    sampler=generation.SAMPLER_K_DPMPP_2M 
    )


now = datetime.now()
filename = now.strftime('%Y-%m-%d-%H-%M-%S') + '.png'

for resp in answers:
    for artifact in resp.artifacts:
        if artifact.finish_reason == generation.FILTER:
            warnings.warn(
                "Your request activated the API's safety filters and could not be processed."
                "Please modify the prompt and try again.")
        if artifact.type == generation.ARTIFACT_IMAGE:
            img = Image.open(io.BytesIO(artifact.binary))
            img.save('./display/img/' + filename)
            plt.imshow(img)
            plt.axis('off')
            plt.show()
            
