import sys
import traceback
import logging
import nltk

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)

def test_nltk_dependencies():
    logger.info("Testing NLTK dependencies...")
    
    try:
        # Check if punkt is available
        logger.info("Checking for punkt tokenizer...")
        try:
            nltk.data.find('tokenizers/punkt')
            logger.info("punkt tokenizer is available")
        except LookupError:
            logger.warning("punkt tokenizer not found, downloading...")
            nltk.download('punkt')
            logger.info("punkt tokenizer downloaded successfully")
        
        # Check if stopwords are available
        logger.info("Checking for stopwords...")
        try:
            nltk.data.find('corpora/stopwords')
            logger.info("stopwords are available")
        except LookupError:
            logger.warning("stopwords not found, downloading...")
            nltk.download('stopwords')
            logger.info("stopwords downloaded successfully")
        
        # Test basic NLTK functionality
        logger.info("Testing basic NLTK functionality...")
        from nltk.tokenize import word_tokenize, sent_tokenize
        test_sentence = "This is a test sentence. This is another test sentence."
        
        logger.info("Testing sentence tokenization...")
        sentences = sent_tokenize(test_sentence)
        logger.info(f"Sentence tokenization result: {sentences}")
        
        logger.info("Testing word tokenization...")
        words = word_tokenize(sentences[0])
        logger.info(f"Word tokenization result: {words}")
        
        from nltk.corpus import stopwords
        logger.info("Testing stopwords...")
        stop_words = set(stopwords.words('english'))
        logger.info(f"First 5 stopwords: {list(stop_words)[:5]}")
        
        logger.info("NLTK dependencies test completed successfully")
        return True
    except Exception as e:
        logger.error(f"Error testing NLTK dependencies: {e}")
        traceback.print_exc()
        return False

def test_summarizers():
    logger.info("Testing summarizers...")
    
    # First test NLTK dependencies
    if not test_nltk_dependencies():
        logger.error("NLTK dependencies test failed, cannot proceed with summarizer tests")
        return
    
    # Import summarizers
    try:
        logger.info("Importing summarizer modules...")
        from models.extractive import ExtractiveTextSummarizer
        from models.abstractive import AbstractiveTextSummarizer
        logger.info("Summarizer modules imported successfully")
    except Exception as e:
        logger.error(f"Error importing summarizer modules: {e}")
        traceback.print_exc()
        return
    
    # Sample text about climate change
    text = """The Impact of Climate Change on Global Ecosystems

Climate change is one of the most pressing challenges of our time, with far-reaching consequences for ecosystems around the world. As global temperatures continue to rise due to the increased concentration of greenhouse gases in the atmosphere, the delicate balance of natural systems is being disrupted.

From the melting polar ice caps to the bleaching of coral reefs, the effects of climate change are evident across diverse habitats. Arctic sea ice is declining at an alarming rate, threatening the survival of polar bears, seals, and other wildlife that depend on it for hunting and breeding. In the oceans, rising temperatures and increasing acidity are causing widespread coral bleaching, destroying the habitats of countless marine species.

Coral reefs, often referred to as the "rainforests of the sea," are particularly vulnerable to climate change. These diverse ecosystems provide habitat for approximately 25% of all marine species, despite covering less than 1% of the ocean floor. The loss of coral reefs not only affects marine biodiversity but also impacts the livelihoods of millions of people who depend on them for food, coastal protection, and tourism.

Terrestrial ecosystems are also experiencing significant changes. Shifting temperature and precipitation patterns are altering the distribution of plant and animal species, with many moving to higher elevations or latitudes in search of suitable conditions. Some species are unable to adapt or migrate quickly enough, leading to population declines and increased extinction risks.

Climate change also disrupts the timing of natural events, such as migration, breeding, and flowering. When these events become misaligned, it can lead to ecological mismatches, where species no longer have access to the resources they need at critical times. For example, birds may arrive at breeding grounds to find that the insects they feed their young have already peaked in abundance.

Forests, which play a crucial role in carbon sequestration, are facing increased threats from wildfires, droughts, and pest outbreaks exacerbated by climate change. The loss of forest cover further contributes to the problem by reducing the Earth's capacity to absorb carbon dioxide.

The impacts of climate change are not limited to wildlife; human communities are also affected. Changes in temperature and precipitation patterns influence agricultural productivity, water availability, and the spread of diseases. Coastal communities face threats from rising sea levels and more intense storms, while those in arid regions may experience more severe droughts.

Addressing the impacts of climate change requires urgent and coordinated action on a global scale. Reducing greenhouse gas emissions, protecting and restoring natural ecosystems, and supporting vulnerable communities are essential steps in mitigating the effects of climate change. Conservation efforts must also focus on enhancing the resilience of ecosystems to help them withstand and adapt to changing conditions.

By working together, we can safeguard the planet's biodiversity and ensure a sustainable future for generations to come. The health of our ecosystems is intrinsically linked to our own well-being, making the protection of these natural systems not just an environmental imperative but a human one as well."""
    
    # Initialize summarizers
    try:
        logger.info("Initializing extractive summarizer...")
        extractive_summarizer = ExtractiveTextSummarizer()
        logger.info("Extractive summarizer initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing extractive summarizer: {e}")
        traceback.print_exc()
        return
    
    try:
        logger.info("Initializing abstractive summarizer...")
        abstractive_summarizer = AbstractiveTextSummarizer()
        logger.info("Abstractive summarizer initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing abstractive summarizer: {e}")
        traceback.print_exc()
        return
    
    # Test extractive summarization
    try:
        logger.info("Testing extractive summarization...")
        extractive_summary = extractive_summarizer.summarize(text, ratio=0.3)
        logger.info("Extractive summary generated successfully")
        logger.info(f"Extractive summary: {extractive_summary}")
    except Exception as e:
        logger.error(f"Error in extractive summarization: {e}")
        traceback.print_exc()
    
    # Test abstractive summarization
    try:
        logger.info("Testing abstractive summarization...")
        abstractive_summary = abstractive_summarizer.summarize(text, ratio=0.3)
        logger.info("Abstractive summary generated successfully")
        logger.info(f"Abstractive summary: {abstractive_summary}")
    except Exception as e:
        logger.error(f"Error in abstractive summarization: {e}")
        traceback.print_exc()
    
    # Compare the two summaries
    logger.info("Comparison between extractive and abstractive summaries:")
    logger.info(f"Extractive summary length: {len(extractive_summary.split())} words")
    logger.info(f"Abstractive summary length: {len(abstractive_summary.split())} words")
    
    logger.info("Summarizer tests completed")

if __name__ == "__main__":
    test_summarizers() 