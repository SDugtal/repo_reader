// Main application JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('repo-form');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const downloadLinks = document.getElementById('download-links');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(form);
        const repoUrl = formData.get('repo_url');
        const formats = formData.getAll('formats');
        
        if (!repoUrl) {
            alert('Please enter a repository URL');
            return;
        }
        
        if (formats.length === 0) {
            alert('Please select at least one output format');
            return;
        }
        
        // Show loading state
        form.classList.add('hidden');
        loading.classList.remove('hidden');
        results.classList.add('hidden');
        
        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    repo_url: repoUrl,
                    formats: formats
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                displayResults(data.result);
            } else {
                throw new Error(data.error || 'Generation failed');
            }
            
        } catch (error) {
            alert('Error: ' + error.message);
            console.error('Error:', error);
        } finally {
            // Hide loading state
            loading.classList.add('hidden');
            form.classList.remove('hidden');
        }
    });

    function displayResults(result) {
        results.classList.remove('hidden');
        
        // Clear previous results
        downloadLinks.innerHTML = '';
        
        // Create download links
        const formats = {
            'markdown': { ext: 'md', icon: '📝', name: 'Markdown' },
            'html': { ext: 'html', icon: '🌐', name: 'HTML' },
            'pdf': { ext: 'pdf', icon: '📄', name: 'PDF' },
            'docx': { ext: 'docx', icon: '📋', name: 'Word Document' }
        };
        
        result.files_generated.forEach(format => {
            const formatInfo = formats[format];
            if (formatInfo) {
                const link = document.createElement('a');
                link.href = `/download/repos_summary.${formatInfo.ext}`;
                link.className = 'download-link';
                link.innerHTML = `
                    <span class="icon">${formatInfo.icon}</span>
                    <span class="name">${formatInfo.name}</span>
                `;
                downloadLinks.appendChild(link);
            }
        });
        
        // Scroll to results
        results.scrollIntoView({ behavior: 'smooth' });
    }
});

// Add some interactive enhancements
document.addEventListener('DOMContentLoaded', function() {
    // Add hover effects to form inputs
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });
    
    // Add loading animation
    const generateBtn = document.querySelector('.generate-btn');
    generateBtn.addEventListener('click', function() {
        this.innerHTML = '<span class="loading-text">Generating...</span>';
        setTimeout(() => {
            this.innerHTML = 'Generate Documentation';
        }, 1000);
    });
});