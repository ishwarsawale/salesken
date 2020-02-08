import scipy.spatial
import re
import tensorflow_hub as hub

module_url = "/Users/ishwarsawale/Downloads/4"
model = hub.load(module_url)


def process_text(text):
    text = text.encode('ascii', errors='ignore').decode()
    text = text.lower()
    text = re.sub(r'http\S+', ' ', text)
    text = re.sub(r'#+', ' ', text )
    text = re.sub(r'@[A-Za-z0-9]+', ' ', text)
    text = re.sub(r"([A-Za-z]+)'s", r"\1 is", text)
    text = re.sub(r"won't", "will not ", text)
    text = re.sub(r"isn't", "is not ", text)
    text = re.sub(r"can't", "can not ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub('\W', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    text = re.sub('\s+', ' ', text)
    text = text.strip()
    return text


def embed(input):
  return model(input)



def get_similar_pair(test, closest_n=2):
    corpus_embeddings = embed(test)
    query_embeddings = embed(test)
    final_list = []
    done_list = []
    for query, query_embedding in zip(test, query_embeddings):
        if query not in done_list:
            query_list = []
            distances = scipy.spatial.distance.cdist([query_embedding], corpus_embeddings, "cosine")[0]
            results = zip(range(len(distances)), distances)
            results = sorted(results, key=lambda x: x[1])

            for idx, distance in results[1:closest_n]:
                predicted = test[idx].strip()
                query_list.append(predicted)
                query_list.append(query)
                done_list.append(query)
                done_list.append(predicted)
                # print(query)
                # print(test[idx].strip(), "(Score: %.4f)" % (1-distance))
            final_list.append(list(set(query_list)))
    return final_list


if __name__ == '__main__':
    test = ["Football is played in Brazil", "i play cricket", "Cricket is played in India",
            "Traveling is good for health", "People love traveling in winter"]

    with open('list_of_sentences', 'r') as f:
        text_list = f.readlines()
    text_list = [process_text(text) for text in text_list]
    print(get_similar_pair(text_list), 2)
