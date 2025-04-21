
# Semantic Analysis of Alice in Wonderland using GloVe and PCA

This project explores the semantic relationships between words in *Alice in Wonderland* by:
- Converting words into vectors using **GloVe embeddings**
- Reducing vector dimensions using **PCA**
- Visualizing semantic proximity via heatmaps and 2D scatter plots

---

## Project Goals

1. **Clean and preprocess the text**
2. **Tokenize and remove unimportant words (stopwords)**
3. **Embed each word into vector space using pre-trained GloVe**
4. **Compute semantic similarity between words**
5. **Visualize relationships using heatmap and PCA**

---

## Workflow

### Step 1: Load and Clean Text
- Access and get `alice.txt` from [Project Gutenberg](https://www.gutenberg.org/ebooks/11)
- Remove headers, footers, and chapter index
- Keep only the main story content

### Step 2: Text Preprocessing
- Convert to lowercase
- Remove punctuation and non-alphabetic characters
- Tokenize text into words
- Remove English stopwords 

### Step 3: Word Embedding with GloVe
- Download GloVe vectors: [`glove.6B.100d.txt`](https://nlp.stanford.edu/projects/glove/)
- Load GloVe and match each word in the text with its 100-dimensional vector

### Step 4: Semantic Analysis
- Select top N most frequent words (e.g. 30)
- Calculate **cosine similarity** between pairs of words
- Create a similarity matrix and draw a heatmap

### Step 5: Dimensionality Reduction with PCA
- Reduce 100D GloVe vectors → 2D
- Visualize words on a 2D plot where:
  - Nearby points = similar meaning
  - Distant points = unrelated meanings

---

## Setup Instructions

### Install Dependencies

```bash
pip install nltk matplotlib seaborn numpy scikit-learn
```

Also, run this to get NLTK data:

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

### Required Files

| File | Description |
|------|-------------|
| `alice.txt` | Source text of Alice in Wonderland |
| `glove.6B.100d.txt` | GloVe word vectors (100d, pre-trained) |
| `GloVe+PCA.ipynb` | Jupyter notebook with full pipeline |
| `README.md` | Project overview |

---

## How to Run

1. Place `alice.txt` and `glove.6B.100d.txt` in the same folder as the notebook.
2. Open `GloVe+PCA.ipynb` in Jupyter or Google Colab.
3. Run the notebook step-by-step:
   - Load and preprocess the text
   - Generate GloVe embeddings
   - Visualize similarity heatmap
   - Apply PCA and plot 2D semantic map

---

## Results
- See the results in the report.pdf file

---

## Notes

- we can customize the number of words, stopwords, and vector dimension.
- Other way to do may be try replace PCA with t-SNE to see how different in visualization.

---

## Credits

- Text from: [Project Gutenberg](https://www.gutenberg.org/ebooks/11)
- Vectors from: [GloVe (Stanford)](https://nlp.stanford.edu/projects/glove/)


