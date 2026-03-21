// Orders.forEach(order => {
//     const tr = document.createElement('tr');
//     const trContent = `
//         <td>${order.productName}</td>
//         <td>${order.productNumber}</td>
//         <td>${order.paymentStatus}</td>
//         <td class="${order.status === 'Declined' ?
//             'danger' : order.status === 'Pending' ? 
//             'warning' : 'primary'}>${order.status}</td>
//         <td class="primary">Details</td>
//     `;
//     tr.innerHTML = trContent;
//     document.querySelector('table tbody').appendChild(tr);    
// });

const ctx = document.getElementById('currencyChart').getContext('2d');
const ctblhd = document.getElementById('currencyHeaders');
const ctbl = document.getElementById('currencyTable');

// This 'fetches' the data from your Python bridge
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

        // new Chart(ctx, {
        //     type: 'line',
        //     data: {
        //         labels: data.labels,
        //         datasets: [{
        //             label: 'Exchange Rate',
        //             data: data.values,
        //             borderColor: '#890295', // Matches your dashboard blue
        //             backgroundColor: 'rgba(172, 44, 201, 0.2)',
        //             fill: true,
        //             tension: 0.3 // Makes the line smooth
        //         }]
        //     },
        //     options: {
        //         responsive: true,
        //         maintainAspectRatio: false,
        //         plugins: {
        //             legend: { display: false }
        //         },
        //         scales: {
        //             y: {
        //                 beginAtZero: false, // Better for currency to see small changes
        //                 grid: { color: 'rgba(0, 0, 0, 0.05)' }
        //             }
        //         }
        //     }
        // });
    )
    .catch(error => console.error('Error loading chart:', error));