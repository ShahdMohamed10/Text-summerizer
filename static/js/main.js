document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('summarize-form');
    const textInput = document.getElementById('text-input');
    const ratioSlider = document.getElementById('ratio-slider');
    const ratioValue = document.getElementById('ratio-value');
    const summarizeBtn = document.getElementById('summarize-btn');
    const resultsCard = document.getElementById('results-card');
    const extractiveContent = document.getElementById('extractive-content');
    const abstractiveContent = document.getElementById('abstractive-content');
    const originalLength = document.getElementById('original-length');
    const extractiveLength = document.getElementById('extractive-length');
    const abstractiveLength = document.getElementById('abstractive-length');
    const copyButtons = document.querySelectorAll('.copy-btn');
    
    // Update ratio value display
    ratioSlider.addEventListener('input', function() {
        ratioValue.textContent = `${this.value}%`;
    });
    
    // Handle form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const text = textInput.value.trim();
        if (!text) {
            alert('Please enter some text to summarize.');
            return;
        }
        
        // Get selected method
        const methodRadios = document.getElementsByName('method');
        let method;
        for (const radio of methodRadios) {
            if (radio.checked) {
                method = radio.value;
                break;
            }
        }
        
        // Get ratio value
        const ratio = parseInt(ratioSlider.value) / 100;
        
        // Show loading state
        summarizeBtn.disabled = true;
        summarizeBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';
        
        // Send request to server
        fetch('/summarize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                method: method,
                ratio: ratio
            }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Display results
            resultsCard.classList.remove('d-none');
            
            // Calculate word counts
            const originalWords = text.split(/\s+/).length;
            originalLength.textContent = `${originalWords} words`;
            
            // Update extractive summary if available
            if (data.extractive) {
                document.getElementById('extractive-tab').classList.remove('d-none');
                extractiveContent.textContent = data.extractive;
                const extractiveWords = data.extractive.split(/\s+/).length;
                extractiveLength.textContent = `${extractiveWords} words (${Math.round(extractiveWords/originalWords*100)}%)`;
            } else {
                document.getElementById('extractive-tab').classList.add('d-none');
            }
            
            // Update abstractive summary if available
            if (data.abstractive) {
                document.getElementById('abstractive-tab').classList.remove('d-none');
                abstractiveContent.textContent = data.abstractive;
                const abstractiveWords = data.abstractive.split(/\s+/).length;
                abstractiveLength.textContent = `${abstractiveWords} words (${Math.round(abstractiveWords/originalWords*100)}%)`;
            } else {
                document.getElementById('abstractive-tab').classList.add('d-none');
            }
            
            // Scroll to results
            resultsCard.scrollIntoView({ behavior: 'smooth' });
            
            // Reset button state
            summarizeBtn.disabled = false;
            summarizeBtn.innerHTML = '<i class="fas fa-magic me-2"></i>Summarize';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while summarizing the text. Please try again.');
            
            // Reset button state
            summarizeBtn.disabled = false;
            summarizeBtn.innerHTML = '<i class="fas fa-magic me-2"></i>Summarize';
        });
    });
    
    // Handle copy buttons
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const textToCopy = document.getElementById(targetId).textContent;
            
            navigator.clipboard.writeText(textToCopy).then(() => {
                // Change button text temporarily
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-check"></i> Copied!';
                setTimeout(() => {
                    this.innerHTML = originalText;
                }, 2000);
            }).catch(err => {
                console.error('Could not copy text: ', err);
            });
        });
    });
    
    // Add example text button (optional)
    const exampleBtn = document.createElement('button');
    exampleBtn.className = 'btn btn-sm btn-outline-secondary mt-2';
    exampleBtn.innerHTML = '<i class="fas fa-lightbulb me-1"></i>Load Example Text';
    exampleBtn.onclick = function() {
        textInput.value = `Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to natural intelligence displayed by animals including humans. AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and takes actions that maximize its chance of achieving its goals.

The term "artificial intelligence" had previously been used to describe machines that mimic and display "human" cognitive skills that are associated with the human mind, such as "learning" and "problem-solving". This definition has since been rejected by major AI researchers who now describe AI in terms of rationality and acting rationally, which does not limit how intelligence can be articulated.

AI applications include advanced web search engines (e.g., Google), recommendation systems (used by YouTube, Amazon and Netflix), understanding human speech (such as Siri and Alexa), self-driving cars (e.g., Waymo), generative or creative tools (ChatGPT and AI art), automated decision-making and competing at the highest level in strategic game systems (such as chess and Go).

As machines become increasingly capable, tasks considered to require "intelligence" are often removed from the definition of AI, a phenomenon known as the AI effect. For instance, optical character recognition is frequently excluded from things considered to be AI, having become a routine technology.`;
    };
    
    // Add the example button after the textarea
    textInput.parentNode.appendChild(exampleBtn);
});