from PIL import Image
import numpy as np

def encode_image(input_image_path, message, output_image_path):
    image = Image.open(input_image_path)
    image = resize_image(image)  # Resize if necessary
    binary_message = ''.join(format(ord(char), '08b') for char in message) + '00000000'  # Append null character
    
    if len(binary_message) > image.size[0] * image.size[1] * 3:
        raise ValueError("Message too long to encode in the image.")
    
    pixels = np.array(image)
    
    binary_message_index = 0
    for i in range(pixels.shape[0]):
        for j in range(pixels.shape[1]):
            for k in range(3):
                if binary_message_index < len(binary_message):
                    pixels[i, j, k] = (pixels[i, j, k] & 0xFE) | int(binary_message[binary_message_index])
                    binary_message_index += 1
    
    encoded_image = Image.fromarray(pixels)
    encoded_image.save(output_image_path)

def decode_image(image_path):
    image = Image.open(image_path)
    pixels = np.array(image)
    
    binary_message = ""
    for i in range(pixels.shape[0]):
        for j in range(pixels.shape[1]):
            for k in range(3):
                binary_message += str(pixels[i, j, k] & 1)
    
    byte_message = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    decoded_message = ''.join(chr(int(byte, 2)) for byte in byte_message)
    
    return decoded_message.split('\x00', 1)[0]  # Remove null character and return message

def resize_image(image, max_size=(800, 800)):
    image.thumbnail(max_size, Image.Resampling.LANCZOS)
    return image
