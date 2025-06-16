document.addEventListener('DOMContentLoaded', function() {
    // Only initialize charts if the elements exist
    if (document.getElementById('monthlyExpensesChart')) {
        initializeMonthlyChart();
    }

    if (document.getElementById('categoryExpensesChart')) {
        initializeCategoryChart();
    }
});

function initializeMonthlyChart() {
    const ctx = document.getElementById('monthlyExpensesChart').getContext('2d');
    const monthsData = JSON.parse(document.getElementById('months-data').textContent);

    const labels = monthsData.map(item => item.month);
    const data = monthsData.map(item => item.amount);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Monthly Expenses',
                data: data,
                backgroundColor: '#4299e1',
                borderColor: '#2b6cb0',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return 'Rp ' + value.toLocaleString();
                        }
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return 'Rp ' + context.raw.toLocaleString();
                        }
                    }
                }
            }
        }
    });
}

function initializeCategoryChart() {
    const ctx = document.getElementById('categoryExpensesChart').getContext('2d');
    const categoriesData = JSON.parse(document.getElementById('categories-data').textContent);

    const labels = categoriesData.map(item => item.category);
    const data = categoriesData.map(item => item.amount);
    const colors = categoriesData.map(item => item.color);

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const value = context.raw;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = Math.round((value / total) * 100);
                            return `${context.label}: Rp ${value.toLocaleString()} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}
