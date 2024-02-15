import utils
import numpy as np

def parse_csv(csv):
    data = {'text': [], 'artists': [], 'bands': []}
    urls = []

    # Process the CSV file
    with open(csv, 'r') as f:
        # Assume first row is field names
        for line in f.readlines()[1:]:
            delim = line.strip().split(',')
            urls.append(delim[0])
            data['artists'].append(delim[1])
            data['bands'].append(delim[2])

    # Scrape URLs for text
    for url in urls:
        print(url)
        data['text'].append(utils.scrape_url_for_text(url))

    return data

def prepare_train_data(file):
    data = parse_csv(file)

    size_train = len(data['text'])
    print('Number of texts:', size_train)
    print('Number of artists:', len(data['artists']))
    print('Number of band lists:', len(data['bands']))

    x_train = []
    y_train = []
    for i in range(size_train):
        x_i, y_i = utils.form_input(data['text'][i], data['artists'][i], data['bands'][i])
        x_train.append(x_i)
        y_train.append(y_i)

    x_train = np.array(x_train)
    y_train = np.array(y_train)

    np.save('x_train.npy', x_train)
    np.save('y_train.npy', y_train)

prepare_train_data('bands.csv')
