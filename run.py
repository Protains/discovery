import numpy as np
from mistralai import Mistral

api_key = 'rP1wYduUYo3dkVeIyOiYQsRRefasjmif'
model = "mistral-embed"

client = Mistral(api_key=api_key)

embeddings_batch_response = client.embeddings.create(
    model=model,
    inputs=["Embed this sentence.", "As well as this one."],
)
print(np.array([embeddings_batch_response.data[i].embedding for i in range(len(embeddings_batch_response.data))]).shape)