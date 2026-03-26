const ctx = document.getElementById('currencyChart').getContext('2d');
const ctbl = document.getElementById('currencyTable');
const darkMode = document.querySelector('.dark-mode');

// Select Sections and Links
const analyticsSection = document.querySelector('.analyse');
const tableSection = document.querySelector('.bank-tables');
const sidebarLinks = document.querySelectorAll('.sidebar a');

//Date Range options for the chart
const filterButtons = document.querySelectorAll('.filter-buttons button');
const currencySelect = document.querySelector('#currencySelect');


let myChart; // Variable to store our chart instance
let currentLimit = 30;
let currentCurrency = 'USD/CAD';

filterButtons.forEach(button => {
    button.addEventListener('click', () => {
        // 1. Get the number from the data attribute
        currentLimit = button.getAttribute('data-limit');

        // 2. Update the UI (moving the active button highlight)
        filterButtons.forEach(btn => btn.classList.remove('active-btn'));
        button.classList.add('active-btn');

        // 3. Call our fetch function with the new limit
        updateChartData(currentCurrency, currentLimit);
        updateTableData(currentCurrency, currentLimit);
        updateSummaryStats(currentCurrency);
    });
});

currencySelect.addEventListener('change', (event) => {
    // 1. Get the value directly from the select element
    currentCurrency = event.target.value;

    // 2. Refresh the data
    updateChartData(currentCurrency, currentLimit);
    updateTableData(currentCurrency, currentLimit);
    updateSummaryStats(currentCurrency);
});

// Set initial state: Start with only the chart visible
tableSection.classList.add('hide');

sidebarLinks.forEach((link, index) => {
    link.addEventListener('click', (e) => {
        e.preventDefault();

        // 1. Manage Active Class in Sidebar
        sidebarLinks.forEach(l => l.classList.remove('active'));
        link.classList.add('active');

        // 2. Toggle Visibility based on index
        // index 0 = Analytics, index 1 = Tables
        if (index === 0) {
            analyticsSection.classList.remove('hide');
            tableSection.classList.add('hide');
            document.querySelector('main h1').textContent = "Analytics";
        } else {
            analyticsSection.classList.add('hide');
            tableSection.classList.remove('hide');
            document.querySelector('main h1').textContent = "Exchange Rate Tables";
        }
    });
});

darkMode.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode-variables');
    darkMode.querySelector('span:nth-child(1)').classList.toggle('active');
    darkMode.querySelector('span:nth-child(2)').classList.toggle('active');
});

fetch('/api/metadata')
    .then(response => response.json())
    .then(data => {
        let option_index = 0;
        data.forEach(item => {
            const opt = document.createElement('option');
            
            // 1. Set the value to the currency label (e.g., 'USD/CAD')
            // opt.value = item.label;
            opt.value = item.series_id;
            
            // 2. Set the visible text
            opt.textContent = `${item.label}: ${item.description}`;
            
            // Set the first item as the default selected currency
            if (option_index === 0) {
                // currentCurrency = item.label;
                currentCurrency = item.series_id;
                opt.selected = true;
            }

            option_index++;
            
            // 3. Add the option to the select element
            currencySelect.appendChild(opt);
        });
        updateChartData(currentCurrency, currentLimit);
        updateTableData(currentCurrency, currentLimit);
        updateSummaryStats(currentCurrency);
    })

function updateChartData(currency, limit) {
    fetch('/api/rates?currency=' + currency + '&limit=' + limit)
        .then(response => response.json())
        .then(data => {

            // If a chart already exists, destroy it first
            if (myChart) {
                myChart.destroy();
            }

            myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Exchange Rate',
                        data: data.values,
                        borderColor: '#890295',
                        fill: true
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false }
            });
        })
        .catch(error => console.error('Error fetching data:', error));
}

function updateTableData(currency, limit) {
    fetch('/api/rates?currency=' + currency + '&limit=' + limit)
        .then(response => response.json())
        .then(data => {

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
        .catch(error => console.error('Error fetching data:', error));
}

function updateSummaryStats(currency) {
    fetch(`/api/summary-stats?currency=${currency}`)
        .then(response => response.json())
        .then(data => {
            // Updating the numbers on the screen
            document.getElementById('stat-average').textContent = data.average;
            document.getElementById('stat-min').textContent = data.min;
            document.getElementById('stat-max').textContent = data.max;
            document.getElementById('stat-range').textContent = data.range;
        })
        .catch(error => console.error('Error fetching summary stats:', error));
}