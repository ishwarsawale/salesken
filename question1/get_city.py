import pandas as pd
import numpy as np


df = pd.read_csv('Correct_cities.csv')
city_list = df["name"]
test_df = pd.read_csv("Misspelt_cities.csv")
city_mis = test_df["misspelt_name"]


def dist(s, t, ratio_calc = False):
    """ levenshtein_ratio_and_distance:
        Calculates levenshtein distance between two strings.
        If ratio_calc = True, the function computes the
        levenshtein distance ratio of similarity between two strings
        For all i and j, distance[i,j] will contain the Levenshtein
        distance between the first i characters of s and the
        first j characters of t
    """
    # Initialize matrix of zeros
    rows = len(s)+1
    cols = len(t)+1
    distance = np.zeros((rows,cols),dtype = int)

    # Populate matrix of zeros with the indeces of each character of both strings
    for i in range(1, rows):
        for k in range(1,cols):
            distance[i][0] = i
            distance[0][k] = k

    # Iterate over the matrix to compute the cost of deletions,insertions and/or substitutions
    for col in range(1, cols):
        for row in range(1, rows):
            if s[row-1] == t[col-1]:
                cost = 0
            else:
                if ratio_calc == True:
                    cost = 2
                else:
                    cost = 1
            distance[row][col] = min(distance[row-1][col] + 1,      # Cost of deletions
                                 distance[row][col-1] + 1,          # Cost of insertions
                                 distance[row-1][col-1] + cost)     # Cost of substitutions
    if ratio_calc == True:
        Ratio = ((len(s)+len(t)) - distance[row][col]) / (len(s)+len(t))
        return Ratio
    else:
        return distance[row][col]


def min_word(word, lst):
  return min((dist(word, w), w) for w in lst)[1]


def process_csv_files():
    corrected_city = []
    corrected_id = []
    for index, row in test_df.iterrows():
        print(f'processing index {index}')
        row_city = row['misspelt_name']
        row_country = row['country']
        train_countries = df.loc[df['country'] == row_country]
        to_check = train_countries['name'].to_list()
        pred_word = min_word(row_city, to_check)
        pred_row = train_countries.loc[train_countries['name'] == pred_word]
        pred_id = pred_row['id'].to_string(index=None, header=None).strip()
        if '\n' in pred_id:
            pred_id = pred_id.replace('\n', '\t')
        print(f'{row_city} -> {pred_word} -> {pred_id}')
        corrected_city.append(pred_word)
        corrected_id.append(pred_id)
    test_df['corrected'] = corrected_city
    test_df['id'] = corrected_id
    test_df.to_csv("new_csv.csv", index=False)


def get_corrected_city(city_name, country):
    train_countries = df.loc[df['country'] == country]
    to_check = train_countries['name'].to_list()
    pred_word = min_word(city_name, to_check)
    pred_row = train_countries.loc[train_countries['name'] == pred_word]
    pred_id = pred_row['id'].to_string(index=None, header=None).strip()
    return pred_id, pred_word


if __name__ == '__main__':
    city = input("City name  ")
    country = input("Country ")
    city_id, pred_city = get_corrected_city(city, country)
    print("\n\n")
    print(f'Input Query is {city} {country}')
    print(f'Corrected city is {pred_city} with id {city_id}')

