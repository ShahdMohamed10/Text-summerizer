import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import numpy as np
import networkx as nx
import re
import string

class ExtractiveTextSummarizer:
    def __init__(self):
        # Download necessary NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
            
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        self.stopwords = set(stopwords.words('english'))
        # Add common words that don't contribute much to meaning
        self.stopwords.update(['also', 'would', 'could', 'may', 'might', 'often', 'usually'])
    
    def summarize(self, text, ratio=0.3):
        """
        Summarize the given text using an enhanced TextRank algorithm.
        
        Args:
            text (str): The text to summarize
            ratio (float): The ratio of the original text to keep
            
        Returns:
            str: The summarized text
        """
        if not text or text.isspace():
            return ""
        
        # Clean and tokenize the text into sentences
        text = self._clean_text(text)
        sentences = sent_tokenize(text)
        
        if not sentences:
            return ""
        
        # If text is short, return it as is
        if len(sentences) <= 3:
            return text
        
        # Create similarity matrix
        similarity_matrix = self._build_similarity_matrix(sentences)
        
        # Rank sentences using PageRank algorithm
        nx_graph = nx.from_numpy_array(similarity_matrix)
        scores = nx.pagerank(nx_graph, alpha=0.85)  # Alpha is the damping factor
        
        # Add position-based weighting (first and last sentences often contain important info)
        position_weight = 0.1
        for i in range(len(sentences)):
            # First few sentences get a boost
            if i < 2:
                scores[i] += position_weight * (2 - i)
            # Last sentence gets a boost
            if i == len(sentences) - 1:
                scores[i] += position_weight
        
        # Sort sentences by score and select top ones
        ranked_sentences = sorted(((scores[i], i, s) for i, s in enumerate(sentences)), reverse=True)
        
        # Calculate the number of sentences to keep
        num_sentences = max(1, int(len(sentences) * ratio))
        
        # Get the top sentences with diversity
        selected_indices = self._ensure_diversity(ranked_sentences, num_sentences)
        
        # Sort selected sentences by their original order
        selected_indices.sort()
        summary_sentences = [sentences[i] for i in selected_indices]
        
        # Join the selected sentences
        summary = ' '.join(summary_sentences)
        
        return summary
    
    def _ensure_diversity(self, ranked_sentences, num_sentences):
        """
        Ensure diversity in the selected sentences by avoiding redundancy.
        
        Args:
            ranked_sentences (list): List of (score, index, sentence) tuples
            num_sentences (int): Number of sentences to select
            
        Returns:
            list: Indices of selected sentences
        """
        selected_indices = []
        selected_sentences = []
        
        # Always include the highest-ranked sentence
        if ranked_sentences:
            _, idx, sentence = ranked_sentences[0]
            selected_indices.append(idx)
            selected_sentences.append(sentence)
        
        # For the rest, ensure diversity
        for _, idx, sentence in ranked_sentences[1:]:
            # Skip if we already have enough sentences
            if len(selected_indices) >= num_sentences:
                break
                
            # Check similarity with already selected sentences
            max_similarity = 0
            for selected in selected_sentences:
                similarity = self._sentence_similarity(sentence, selected)
                max_similarity = max(max_similarity, similarity)
            
            # If similarity is below threshold, include this sentence
            if max_similarity < 0.5:  # Adjust threshold as needed
                selected_indices.append(idx)
                selected_sentences.append(sentence)
        
        # If we don't have enough sentences, add more from the ranked list
        remaining = [r for r in ranked_sentences if r[1] not in selected_indices]
        for _, idx, sentence in remaining:
            if len(selected_indices) >= num_sentences:
                break
            selected_indices.append(idx)
        
        return selected_indices
    
    def _clean_text(self, text):
        """
        Clean the text by removing extra whitespace and normalizing.
        
        Args:
            text (str): The text to clean
            
        Returns:
            str: The cleaned text
        """
        # Replace multiple newlines with a single space
        text = re.sub(r'\n+', ' ', text)
        # Replace multiple spaces with a single space
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _build_similarity_matrix(self, sentences):
        """
        Build a similarity matrix for the given sentences.
        
        Args:
            sentences (list): List of sentences
            
        Returns:
            numpy.ndarray: Similarity matrix
        """
        # Number of sentences
        n = len(sentences)
        
        # Initialize similarity matrix
        similarity_matrix = np.zeros((n, n))
        
        # Calculate similarity between each pair of sentences
        for i in range(n):
            for j in range(n):
                if i != j:
                    similarity_matrix[i][j] = self._sentence_similarity(sentences[i], sentences[j])
        
        return similarity_matrix
    
    def _sentence_similarity(self, sent1, sent2):
        """
        Calculate similarity between two sentences using an improved method.
        
        Args:
            sent1 (str): First sentence
            sent2 (str): Second sentence
            
        Returns:
            float: Similarity score
        """
        try:
            # Clean and normalize sentences
            sent1 = self._normalize_sentence(sent1)
            sent2 = self._normalize_sentence(sent2)
            
            # Split into words and filter stopwords
            words1 = [word for word in sent1.split() if word not in self.stopwords]
            words2 = [word for word in sent2.split() if word not in self.stopwords]
            
            # If either sentence has no meaningful words, return 0
            if not words1 or not words2:
                return 0
            
            # Create sets for faster operations
            set1 = set(words1)
            set2 = set(words2)
            
            # Calculate Jaccard similarity (intersection over union)
            intersection = len(set1.intersection(set2))
            union = len(set1.union(set2))
            
            if union == 0:
                return 0
            
            # Calculate TF-IDF weighted similarity
            common_words = set1.intersection(set2)
            
            # Simple TF weighting: longer words often carry more meaning
            weight_sum = sum(len(word) for word in common_words)
            max_weight = sum(len(word) for word in set1.union(set2))
            
            if max_weight == 0:
                return 0
            
            # Combine Jaccard similarity with weighted similarity
            jaccard = intersection / union
            weighted = weight_sum / max_weight
            
            return 0.7 * jaccard + 0.3 * weighted
            
        except Exception as e:
            print(f"Error in sentence similarity calculation: {e}")
            return 0
    
    def _normalize_sentence(self, sentence):
        """
        Normalize a sentence by removing punctuation and converting to lowercase.
        
        Args:
            sentence (str): The sentence to normalize
            
        Returns:
            str: The normalized sentence
        """
        # Convert to lowercase
        sentence = sentence.lower()
        
        # Remove punctuation
        sentence = sentence.translate(str.maketrans('', '', string.punctuation))
        
        return sentence