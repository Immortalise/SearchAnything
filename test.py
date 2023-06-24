from sentence_transformers import SentenceTransformer, util
from PIL import Image
import torch
import numpy as np

#Load CLIP model
model = SentenceTransformer('clip-ViT-B-32')

#Encode an image:
# img_emb = model.encode(Image.open('/home/haoc/Anything/images/panda1.png'))
img_emb1 = model.encode(Image.open('/home/haoc/Anything/images/panda1.png'))
img_emb2 = model.encode(Image.open('/home/haoc/Anything/images/panda2.jpg'))
img_emb3 = model.encode(Image.open('/home/haoc/Anything/images/panda4.png'))
img_emb4 = model.encode(Image.open('/home/haoc/Anything/images/panda5.png'))
img_emb5 = model.encode(Image.open('/home/haoc/Anything/images/panda6.png'))
img_emb6 = model.encode(Image.open('/home/haoc/Anything/images/panda7.png'))
img_emb7 = model.encode(Image.open('/home/haoc/Anything/images/cartoon_panda1.png'))
img_emb8 = model.encode(Image.open('/home/haoc/Anything/images/cartoon_panda2.png'))
img_emb9 = model.encode(Image.open('/home/haoc/Anything/images/cartoon_panda3.png'))

tensor_list = [img_emb1, img_emb2, img_emb3, img_emb4, img_emb5, img_emb6, img_emb7, img_emb8, img_emb9]

stacked_ndarray = np.stack(tensor_list)
img_emb = torch.from_numpy(stacked_ndarray)

print(type(img_emb))
print(img_emb.shape)
#Encode text descriptions
text_emb = model.encode('panda on the tree')
print(text_emb.shape)
#Compute cosine similarities 
cos_scores = util.cos_sim(img_emb, text_emb)
print(cos_scores)