import pickle
import random
import json

with open('humor_label_sdk.pkl', 'rb') as f:
    labels = pickle.load(f)
with open('language_sdk.pkl', 'rb') as f:
    sentences = pickle.load(f)

prompts = []
for k in sentences: 
    full = '. '.join(sentences[k]['context_sentences'])+'. '+sentences[k]['punchline_sentence']+'.<start>'
    label = labels[k]
    prompt = {'prompt': full}
    prompt['completion'] = 'FUNNY<end>' if label else 'SERIOUS<end>'
    prompts.append(prompt)
random.shuffle(prompts)
prompts = [json.dumps(x) for x in prompts]
train_set= '\n'.join(prompts[:8000]) 
test_set = '\n'.join(prompts[8000:])
# haha yes sklearn does exist
# but what if instead i didn't
with open('silly_gpt3_jokes.jsonl', 'w') as f:
    f.write(train_set)
with open('silly_gpt3_jokes_test.jsonl', 'w') as f:
    f.write(test_set)
