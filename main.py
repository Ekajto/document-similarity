from data_cleaning import clean_data
from data_evaluation import calculate_similarity
from data_extractor import extract_data
from data_processing import process_data
from util import create_table

links = [
    "https://wolnelektury.pl/media/book/txt/serce-lasowiackie.txt",
    "https://wolnelektury.pl/media/book/txt/asbe.txt",
    "https://wolnelektury.pl/media/book/txt/dwuglos-milosci.txt",
    "https://wolnelektury.pl/media/book/txt/dafne-swietochowski.txt",
]

if __name__ == "__main__":
    replaced_tokens_list = []
    headers = []
    for link in links:
        header = link.split("/txt/")[1].split(".txt")[0]
        headers.append(header)
        text = extract_data(link)
        tokens = clean_data(text)
        replaced_tokens_list.append(process_data(tokens))
    matrix = calculate_similarity(replaced_tokens_list)
    print(create_table(matrix, headers))
