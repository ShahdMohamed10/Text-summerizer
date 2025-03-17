import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
import numpy as np
import re
import string
import heapq
import random

class AbstractiveTextSummarizer:
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
    
    def summarize(self, text, ratio=0.3):
        """
        Summarize the given text using a frequency-based approach.
        
        Args:
            text (str): The text to summarize
            ratio (float): The ratio of the original text to keep
            
        Returns:
            str: The summarized text
        """
        try:
            if not text or text.isspace():
                return ""
            
            # Clean the text
            cleaned_text = self._clean_text(text)
            
            # Tokenize the text into sentences
            sentences = sent_tokenize(cleaned_text)
            
            if not sentences:
                return ""
            
            # If text is short, return it as is
            if len(sentences) <= 3:
                return text
            
            # Calculate word frequencies
            word_frequencies = self._calculate_word_frequencies(cleaned_text)
            
            # Calculate sentence scores based on word frequencies
            sentence_scores = {}
            for i, sentence in enumerate(sentences):
                score = self._score_sentence(sentence, word_frequencies)
                # Add position bias (first and last sentences often contain important info)
                if i < 2:  # First two sentences
                    score *= 1.2
                elif i == len(sentences) - 1:  # Last sentence
                    score *= 1.1
                sentence_scores[sentence] = score
            
            # Calculate the number of sentences to keep
            num_sentences = max(1, int(len(sentences) * ratio))
            
            # Get the top sentences
            summary_sentences = heapq.nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
            
            # Reorder sentences to maintain original flow
            ordered_summary = []
            for sentence in sentences:
                if sentence in summary_sentences:
                    ordered_summary.append(sentence)
            
            # Enhance coherence between sentences
            enhanced_summary = self._enhance_coherence(ordered_summary)
            
            # Join the selected sentences
            summary = ' '.join(enhanced_summary)
            
            return summary
        except Exception as e:
            print(f"Error in abstractive summarization: {e}")
            return "Error generating summary. Please try again."
    
    def _enhance_coherence(self, sentences):
        """
        Enhance coherence between sentences by adding transition words where appropriate.
        
        Args:
            sentences (list): List of sentences
            
        Returns:
            list: List of sentences with enhanced coherence
        """
        if len(sentences) <= 1:
            return sentences
        
        enhanced = [sentences[0]]
        
        # Transition words for different relationships
        additions = ["Additionally", "Furthermore", "Moreover"]
        contrasts = ["However", "In contrast", "On the other hand"]
        causes = ["Therefore", "As a result", "Consequently"]
        
        for i in range(1, len(sentences)):
            current = sentences[i]
            previous = sentences[i-1]
            
            # Skip if sentence already starts with a transition word
            if any(current.startswith(word) for word in additions + contrasts + causes):
                enhanced.append(current)
                continue
            
            # Simple heuristic: check for contrast words
            contrast_indicators = ["but", "however", "although", "yet", "despite"]
            if any(word in current.lower() for word in contrast_indicators):
                transition = random.choice(contrasts)
                enhanced.append(f"{transition}, {current}")
            # Check for cause-effect relationship
            elif any(word in current.lower() for word in ["therefore", "thus", "hence", "so"]):
                transition = random.choice(causes)
                enhanced.append(f"{transition}, {current}")
            # Default to addition
            elif random.random() < 0.3:  # Only add transitions sometimes
                transition = random.choice(additions)
                enhanced.append(f"{transition}, {current}")
            else:
                enhanced.append(current)
        
        return enhanced
    
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
    
    def _calculate_word_frequencies(self, text):
        """
        Calculate the frequency of each word in the text.
        
        Args:
            text (str): The text to analyze
            
        Returns:
            dict: Word frequencies
        """
        # Normalize text
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Split into words
        words = text.split()
        
        # Remove stopwords
        words = [word for word in words if word not in self.stopwords]
        
        # Calculate frequencies
        word_frequencies = {}
        for word in words:
            if word in word_frequencies:
                word_frequencies[word] += 1
            else:
                word_frequencies[word] = 1
        
        # Normalize frequencies
        max_frequency = max(word_frequencies.values()) if word_frequencies else 1
        for word in word_frequencies:
            word_frequencies[word] = word_frequencies[word] / max_frequency
        
        return word_frequencies
    
    def _score_sentence(self, sentence, word_frequencies):
        """
        Score a sentence based on the frequency of its words.
        
        Args:
            sentence (str): The sentence to score
            word_frequencies (dict): Word frequencies
            
        Returns:
            float: Sentence score
        """
        # Normalize sentence
        sentence = sentence.lower()
        sentence = sentence.translate(str.maketrans('', '', string.punctuation))
        
        # Split into words
        words = sentence.split()
        
        # Remove stopwords
        words = [word for word in words if word not in self.stopwords]
        
        # Calculate score
        score = 0
        for word in words:
            if word in word_frequencies:
                score += word_frequencies[word]
        
        # Normalize by sentence length to avoid bias towards longer sentences
        # Add 1 to avoid division by zero
        return score / (len(words) + 1)
    
    def chunk_text(self, text, max_chunk_size=1000):
        """
        Split text into chunks to handle long texts.
        
        Args:
            text (str): The text to chunk
            max_chunk_size (int): Maximum size of each chunk
            
        Returns:
            list: List of text chunks
        """
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = []
        current_size = 0
        
        for sentence in sentences:
            sentence_size = len(sentence)
            if current_size + sentence_size <= max_chunk_size:
                current_chunk.append(sentence)
                current_size += sentence_size
            else:
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_size = sentence_size
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
            
        return chunks