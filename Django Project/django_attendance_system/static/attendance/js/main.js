document.addEventListener("DOMContentLoaded", function () {
  const monthlyEl = document.getElementById("monthlyChart");
  if (monthlyEl && window.__monthlyLabels && window.__monthlyValues) {
    new Chart(monthlyEl, {
      type: "line",
      data: {
        labels: window.__monthlyLabels,
        datasets: [{
          label: "Present",
          data: window.__monthlyValues
        }]
      }
    });
  }

  const allPresent = document.getElementById("markAllPresent");
  const allAbsent = document.getElementById("markAllAbsent");

  function toggleRow(row, value) {
    const present = row.querySelector(".status-present");
    const absent = row.querySelector(".status-absent");
    if (!present || !absent) return;
    if (value === "Present") {
      present.checked = true;
      absent.checked = false;
    } else {
      absent.checked = true;
      present.checked = false;
    }
  }

  document.querySelectorAll("tr").forEach((row) => {
    const present = row.querySelector(".status-present");
    const absent = row.querySelector(".status-absent");
    if (present && absent) {
      present.addEventListener("change", () => {
        if (present.checked) absent.checked = false;
      });
      absent.addEventListener("change", () => {
        if (absent.checked) present.checked = false;
      });
    }
  });

  if (allPresent) {
    allPresent.addEventListener("click", () => {
      document.querySelectorAll(".status-present").forEach((el) => {
        el.checked = true;
        const row = el.closest("tr");
        if (row) toggleRow(row, "Present");
      });
    });
  }
  if (allAbsent) {
    allAbsent.addEventListener("click", () => {
      document.querySelectorAll(".status-absent").forEach((el) => {
        el.checked = true;
        const row = el.closest("tr");
        if (row) toggleRow(row, "Absent");
      });
    });
  }
});
