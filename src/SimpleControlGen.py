#!git clone https://github.com/Textbot/OpenTextbot

import numpy as np
import OpenTextbot.src.Algebra as Algebra


def SimplyControlledGen(model, bpe, texts, length=100, top_k=10, temperature=1.0, words):

'''Generate text after the given contexts mentioning some controlled semantics.

    :param model: The trained model.
    :param bpe: Byte pair encoding object.
    :param texts: A list of texts.
    :param length: The length of following texts to be generated.
    :param top_k: Choose the next token from top K.
    :param temperature: Randomness in boltzmann distribution.
    :param words(list(str)): list of words which semantics should be mentioned in the generated text;
    :return: A list of generated texts.
    
   Example:
    texts = ['Mother cleaned the chair, table and the floor.']
    words = ['table']
'''

    ListWeight = model.layers[1].get_weights()
    ListWE = ListWeight[0]
    ArrayWE = np.asarray(ListWE)

    batch_size = len(texts)
    encodes = [bpe.encode(text) for text in texts]
    text_lens = [len(encode) for encode in encodes]
    max_len = max(text_lens)
    input_data = [encode + [0] * (max_len - len(encode)) for encode in encodes]
    encodes_words = [bpe.encode(word) for word in words]
    for shift in range(length):
        output_data = model.predict(np.array(input_data))
        for index in range(batch_size):
            probs = [(prob, i) for i, prob in enumerate(output_data[index, text_lens[index] + shift - 1])]
            probs.sort(reverse=True)
            probs = probs[:top_k]
            indices, probs = list(map(lambda x: x[1], probs)), list(map(lambda x: x[0], probs))
            probs = np.array(probs) / temperature
            probs = probs - np.max(probs)
            probs = np.exp(probs)
            probs = probs / np.sum(probs)
            
            next_token = np.random.choice(indices, p=probs)
            if(len(encodes_words) > 0):
                BPE = encodes_words[0]
                WE = ArrayWE[BPE]
                WE = WE[0]
                ArrayWEindices = ArrayWE[indices]
                ArrayWEindices = np.array(ArrayWEindices)
                ID = Algebra.EuclidianMax(ArrayWEindices, WE)
                LD = Algebra.Euclidian([ArrayWEindices[ID]], WE)
                if (LD[0] < (1.7)):
                  next_token = ID
                  print(shift)
                  encodes_words.remove(encodes_words[0])
            input_data[index].append(0)
            input_data[index][text_lens[index] + shift] = next_token
    outputs = [bpe.decode(input_data[index][:text_lens[index] + length]) for index in range(batch_size)]

    return outputs
