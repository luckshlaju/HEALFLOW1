function updateTime() {
    const now = new Date();
    const timeString = now.toLocaleString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit',
        hour12: true,
        month: 'short',
        day: 'numeric',
        year: 'numeric'
    });
    
    const timeElements = document.querySelectorAll('#current-time');
    timeElements.forEach(el => {
        el.textContent = timeString;
    });
}

setInterval(updateTime, 1000);
updateTime();

document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
});
// ---------------- SUPPLY CHAIN DATA ----------------

document.addEventListener("DOMContentLoaded", () => {
    loadSupplyStats();
    loadSupplyInventory();
    loadSupplyPredictions();
});

// ---- TOP CARDS ----
function loadSupplyStats() {
    fetch("/api/supply/stats")
        .then(res => res.json())
        .then(data => {
            setText("total-items", data.totalItems);
            setText("critical-items", data.criticalItems);
            setText("auto-orders", data.autoOrdersPending);
            setText("monthly-spend", "$" + data.monthlySpend.toLocaleString());
        })
        .catch(err => console.error("Supply stats error:", err));
}

// ---- INVENTORY TABLE ----
function loadSupplyInventory() {
    fetch("/api/supply/inventory")
        .then(res => res.json())
        .then(items => {
            const tbody = document.querySelector("#inventory-table-body");
            if (!tbody) return;

            tbody.innerHTML = "";

            items.forEach(item => {
                tbody.innerHTML += `
                    <tr>
                        <td>${item.name}<br><small>${item.supplier}</small></td>
                        <td>${item.currentStock}/${item.minRequired}</td>
                        <td>${item.daysRemaining} days</td>
                        <td><span class="badge ${item.status.toLowerCase()}">${item.status}</span></td>
                    </tr>
                `;
            });
        })
        .catch(err => console.error("Inventory error:", err));
}

// ---- SHORTAGE PREDICTIONS ----
function loadSupplyPredictions() {
    fetch("/api/supply/predictions")
        .then(res => res.json())
        .then(predictions => {
            const container = document.querySelector("#shortage-predictions");
            if (!container) return;

            container.innerHTML = "";

            predictions.forEach(p => {
                container.innerHTML += `
                    <div class="alert">
                        <strong>${p.item}</strong><br>
                        Shortage Date: ${p.shortageDate}<br>
                        Recommended Order: ${p.recommendedOrder}<br>
                        Estimated Cost: $${p.estimatedCost.toLocaleString()}
                    </div>
                `;
            });
        })
        .catch(err => console.error("Predictions error:", err));
}

// ---- HELPER ----
function setText(id, value) {
    const el = document.getElementById(id);
    if (el) el.textContent = value;
}
// ---------------- BED & STAFF AUTO OPTIMIZE ----------------

document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("auto-optimize-btn");
    if (btn) {
        btn.addEventListener("click", autoOptimizeBeds);
    }
});

function autoOptimizeBeds() {
    fetch("/api/beds/allocate", {
        method: "POST",
        headers: { "Content-Type": "application/json" }
    })
    .then(res => res.json())
    .then(data => {
        const tbody = document.getElementById("allocation-table-body");
        if (!tbody) return;

        tbody.innerHTML = "";

        data.forEach(row => {
            tbody.innerHTML += `
                <tr>
                    <td>${row.department}</td>
                    <td>${row.total_beds}</td>
                    <td>${row.occupied_beds}</td>
                    <td>${row.available_beds}</td>
                    <td>${row.utilization}%</td>
                    <td>${row.recommendation ?? "—"}</td>
                </tr>
            `;
        });
    })
    .catch(err => console.error("Auto optimize error:", err));
}
