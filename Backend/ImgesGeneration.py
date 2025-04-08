# import asyncio
# from random import randint 
# from PIL import Image 
# from requests
# from dotenv import get_key
# import os
# from time import sleep 

# def open_image(prompt):
#     folder_path = r"Data"
#     prompt = prompt.replace(" ", "_")

#     Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

#     for jpg_file in Files:
#         image_path = os.path.join(folder_path, jpg_file)

#         try:
#             img = Image.open(image_path)
#             print(f"Opening image: {image_path}")
#             img.show()
#             sleep(1)
#         except IOError:
#             print(f"Unable to open {image_path}")

# API_URL=""
# headers={"Authoriation":f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}

# # Async function to send a query to the huggig face API
# async def query(playload):
#     response= await asyncio.to_thread(requests.post, API_URL, headers=headers, json= playload)
#     return response.content

# # Aysnc function to genrate images based on the given prompt
# async def geerate_images(prompt: str):
#     tasks=[]

#     for _ in range(4):
#         playload={
        
#         }