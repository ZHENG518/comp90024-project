import json

with open('SA3-language.json', 'r') as f:
    language_data = json.load(f)

new_features = []
language_count = {}
for feature in language_data['features']:
    properties = feature['properties']
    new_properties = {'name':properties['SA3_NAME11'], 'total_persons':properties['SEO_Persons']}
    for key, value in properties.items():
        if key.startswith('SOL'):
            language = key.split('_')[1]
            if language == 'Chin':
                language = 'Chinese'
            new_properties[language+'_persons'] = value
            language_count[language] = language_count.get(language,0)+value
        elif key.startswith('SEO'):
            new_properties['English_persons'] = value
            language_count['English'] = language_count.get('English',0)+value
    feature['properties'] = new_properties
    new_features.append(feature)
language_data['features'] = new_features

for feature in language_data['features']:
    percentages = {}
    for key, value in feature['properties'].items():
        language = key.split('_')[0]
        if language not in ['name','total']:
            percentages[language+'_persons_percentage'] = float('%.4f' % (value/language_count[language]))
    feature['properties'].update(percentages)

with open('./language_data.json', 'w') as f:
    json.dump(language_data, f, indent=2)

print('hhh')