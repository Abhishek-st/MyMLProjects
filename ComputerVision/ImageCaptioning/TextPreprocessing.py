# -*- coding: utf-8 -*-


import os
import string

def load_doc(filename):
  file = open(filename, 'r')
  text = file.read()
  file.close()
  return text

line = load_doc('/Image_caption/Flickr8k.token.txt')
# split line by white space
tokens = line.split()
# take the first token as the image id, the rest as the description
image_id, image_desc = tokens[0], tokens[1:]

image_id = image_id.split('.')[0]
image_desc = ' '.join(image_desc)

print(type(image_id))
print(type(image_desc[:10]))

# loading  tokens and mapping
def load_descriptions(doc):
	mapping = dict()
	# process lines
	for line in doc.split('\n'):
		# split line by white space
		tokens = line.split()
		if len(line) < 2:
			continue
		# take the first token as the image id, the rest as the description
		image_id, image_desc = tokens[0], tokens[1:]
		# remove filename from image id
		image_id = image_id.split('.')[0]
		# convert description tokens back to string
		image_desc = ' '.join(image_desc)
		# store the first description for each image
		if image_id not in mapping:
			mapping[image_id] = image_desc
	return mapping

filename = 'Flickr8k.token.txt'
doc = load_doc(filename)
descriptions = load_descriptions(doc)
print(f'Loaded: {len(descriptions)}')

print(type(descriptions))

# clean description text
def clean_descriptions(descriptions):
	# prepare translation table for removing punctuation
	table = str.maketrans('', '', string.punctuation)
	for key, desc in descriptions.items():
		# tokenize
		desc = desc.split()
		# convert to lower case
		desc = [word.lower() for word in desc]
		# remove punctuation from each token
		desc = [w.translate(table) for w in desc]
		# remove hanging 's' and 'a'
		desc = [word for word in desc if len(word)>1]
		# store as string
		descriptions[key] =  ' '.join(desc)

# save descriptions to file, one per line
def save_doc(descriptions, filename):
	lines = list()
	for key, desc in descriptions.items():
		lines.append(key + ' ' + desc)
	data = '\n'.join(lines)
	file = open(filename, 'w')
	file.write(data)
	file.close()

clean_descriptions(descriptions)

all_tokens = ' '.join(descriptions.values()).split()
vocabulary = set(all_tokens)
print('Vocabulary Size: %d' % len(vocabulary))

save_doc(descriptions, 'descriptions.txt')


