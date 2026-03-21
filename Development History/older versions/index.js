const ctx = document.getElementById('currencyChart').getContext('2d');
const ctbl = document.getElementById('currencyTable');
const sideMenu = document.querySelector('aside');
const menuBtn = document.getElementById('menu-btn');
const closeBtn = document.getElementById('close-btn');
const darkMode = document.querySelector('.dark-mode');

// Toggle Dark Mode
darkMode.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode-variables');
    darkMode.querySelector('span:nth-child(1)').classList.toggle('active');
    darkMode.querySelector('span:nth-child(2)').classList.toggle('active');
})

fetch('http://127.0.0.1:5000/api/rates')
    .then(response => response.json())
    .then(data => {
        // 1. Update the Chart
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Exchange Rate',
                    data: data.values,
                    borderColor: '#890295',
                    backgroundColor: 'rgba(172, 44, 201, 0.2)',
                    fill: true,
                    tension: 0.3
                }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });

        // 2. Clear and fill the Table
        ctbl.innerHTML = ''; 
        data.all_data.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${row.date}</td>
                <td>${row.currency}</td>
                <td>${row.rate}</td>
                <td>${row.description}</td>
            `;
            ctbl.appendChild(tr);
        });
    })
    .catch(error => console.error('Error loading data:', error));   