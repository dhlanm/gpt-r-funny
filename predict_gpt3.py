import openai
import json

openai.api_key = "i'm not uploading this to github"

with open('silly_gpt3_jokes_test.jsonl') as f:
    test_set = [json.loads(x) for x in f.read().split('\n') if x]

good_answers = ['SERIOUS', 'FUNNY']

correct = 0
valid = 0
funny = 0
true_positives = 0
for test in test_set: 
    prompt = test['prompt']
    answer = test['completion'][:-5]
    # manually add finetune model name
    # result of openai api fine_tunes.create -t silly_gpt3_jokes.jsonl -m curie 
    # ~$7 of api token usage
    completion = openai.Completion.create(model="curie:ft-user-gbqhx0wfif8m4g2kkkhf6aur-2021-08-06-04-30-07", prompt=prompt, stop="<end>")
    guess = completion.choices[0].text
    if answer == 'FUNNY': 
        funny += 1
    if guess == answer: 
        correct += 1
        if answer == 'FUNNY': 
            true_positives += 1
    if guess in good_answers: 
        valid += 1

print(f'{correct}/{len(test_set)} correct classifications = {(correct/len(test_set)) * 100}% accuracy')

true_negatives = correct - true_positives
false_negatives = funny - true_positives
false_positives = len(test_set) - correct - false_negatives

print(f'tp: {true_positives}    fp: {false_positives}')
print(f'tn: {true_negatives}    fn: {false_negatives}')
recall = true_positives/funny
print(f'{true_positives}/{funny} true positives = {recall} recall')
precision = true_positives / (true_positives + false_negatives)
print(f'{true_positives}/{true_positives + false_negatives} = {precision} precision')
print(f'{(2 * precision * recall) / (precision + recall)} f-score')

print(f'{valid}/{len(test_set)} valid answers')
