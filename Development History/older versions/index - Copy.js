Orders.forEach(order => {
    const tr = document.createElement('tr');
    const trContent = `
        <td>${order.productName}</td>
        <td>${order.productNumber}</td>
        <td>${order.paymentStatus}</td>
        <td class="${order.status === 'Declined' ?
            'danger' : order.status === 'Pending' ? 
            'warning' : 'primary'}>${order.status}</td>
        <td class="primary">Details</td>
    `;
    tr.innerHTML = trContent;
    document.querySelector('table tbody').appendChild(tr);    
});

const ctx = document.getElementById('currencyChart').getContext('2d');

fetch('http://127.0.0.1:5000/api/rates')
    .then(response => response.json())
    .then(data => {
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'USD to CAD',
                    data: data.values,
                    borderColor: '#6C9BCF', // Matching the dashboard's blue theme
                    tension: 0.3,
                    fill: true,
                    backgroundColor: 'rgba(108, 155, 207, 0.1)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                }
            }
        });
    });