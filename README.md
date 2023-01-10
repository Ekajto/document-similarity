# Document normalization and comparison

Project that uses some books from https://wolnelektury.pl/katalog/ and uses Levenshtein algorithm to normalize and compare documents.

It is divided for 4 parts

- `data_extractor`.py that is responsible for getting text from provided link
- `data_cleaning` that is responsible for getting rid of uneccesarry text not related to book, polish stopwords (that are define in `polish_stopwords.txt`) and other uneccesarry characters
- `data_processing` that is responsible for groupping similar words, choosing representative of that words and replacing source tokens using Levenshtein algorithm
- `data_evaluation` that is responsible for calulcating similarity between provided books using Levenshtein algorithm

To run code with already provided books and installed dependencies in your venv just run
`python -m main`
