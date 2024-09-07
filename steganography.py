from PIL import Image
import numpy as np

def text_to_bin(text):
    return ''.join(format(ord(char), '08b') for char in text)

def bin_to_text(binary):
    text = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
    return text

def encode_image(input_image_path, output_image_path, secret_message):
    image = Image.open(input_image_path)
    np_image = np.array(image)

    binary_message = text_to_bin(secret_message) + '1111111111111110'
    binary_message_length = len(binary_message)

    data_index = 0
    for row in np_image:
        for pixel in row:
            for channel in range(3):
                if data_index < binary_message_length:
                    pixel[channel] = int(format(pixel[channel], '08b')[:-1] + binary_message[data_index], 2)
                    data_index += 1

    encoded_image = Image.fromarray(np_image)
    encoded_image.save(output_image_path)
    print(f"Message encoded and saved to {output_image_path}")

def decode_image(encoded_image_path):
    image = Image.open(encoded_image_path)
    np_image = np.array(image)

    binary_message = ""
    for row in np_image:
        for pixel in row:
            for channel in range(3):
                binary_message += format(pixel[channel], '08b')[-1]

    binary_message = binary_message.split('1111111111111110')[0]
    secret_message = bin_to_text(binary_message)
    return secret_message

if __name__ == "__main__":
    # Encode
    input_image = "input_image.png"
    output_image = "output_image.png"
    secret_message = "This is a hidden message."

    encode_image(input_image, output_image, secret_message)

    # Decode
    decoded_message = decode_image(output_image)
    print("Decoded message:", decoded_message)
