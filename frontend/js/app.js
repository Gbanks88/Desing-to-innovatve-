// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Utility Functions
function createCard(item, type) {
    const card = document.createElement('div');
    card.className = 'card';
    
    let tagsHtml = '';
    if (item.tags) {
        tagsHtml = `
            <div class="tags">
                ${item.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
            </div>
        `;
    }

    let content = '';
    switch(type) {
        case 'fashion':
            content = `
                <img src="${item.image || 'https://via.placeholder.com/300x200'}" alt="${item.title}" class="card-image">
                <div class="card-content">
                    <h3>${item.title}</h3>
                    <p>${item.description}</p>
                    ${tagsHtml}
                    <div class="items">
                        ${item.items ? item.items.map(i => `
                            <div class="item">
                                <span>${i.name}</span>
                                <span>$${i.price}</span>
                            </div>
                        `).join('') : ''}
                    </div>
                </div>
            `;
            break;
        
        case 'video':
            content = `
                <img src="${item.thumbnail || 'https://via.placeholder.com/300x200'}" alt="${item.title}" class="card-image">
                <div class="card-content">
                    <h3>${item.title}</h3>
                    <p>${item.description}</p>
                    <p class="duration">Duration: ${item.duration}</p>
                    ${tagsHtml}
                </div>
            `;
            break;
        
        case 'scholarship':
            content = `
                <div class="card-content">
                    <h3>${item.title}</h3>
                    <p>${item.description}</p>
                    <div class="scholarship-details">
                        <p class="amount">Amount: $${item.amount.toLocaleString()}</p>
                        <p class="deadline">Deadline: ${new Date(item.deadline).toLocaleDateString()}</p>
                    </div>
                    <div class="requirements">
                        <h4>Requirements:</h4>
                        <ul>
                            ${item.requirements.map(req => `<li>${req}</li>`).join('')}
                        </ul>
                    </div>
                    ${tagsHtml}
                </div>
            `;
            break;
    }

    card.innerHTML = content;
    return card;
}

async function fetchData(endpoint) {
    try {
        const response = await fetch(`${API_BASE_URL}/${endpoint}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(`Error fetching ${endpoint}:`, error);
        return [];
    }
}

// Load Content Functions
async function loadFashionItems() {
    const items = await fetchData('fashion');
    const container = document.getElementById('fashion-items');
    container.innerHTML = '';
    items.forEach(item => {
        container.appendChild(createCard(item, 'fashion'));
    });
}

async function loadVideos() {
    const videos = await fetchData('videos');
    const container = document.getElementById('video-items');
    container.innerHTML = '';
    videos.forEach(video => {
        container.appendChild(createCard(video, 'video'));
    });
}

async function loadScholarships() {
    const scholarships = await fetchData('scholarships');
    const container = document.getElementById('scholarship-items');
    container.innerHTML = '';
    scholarships.forEach(scholarship => {
        container.appendChild(createCard(scholarship, 'scholarship'));
    });
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadFashionItems();
    loadVideos();
    loadScholarships();
});
