const button = document.getElementById('refresh');
const status = document.getElementById('status');
const table = document.querySelector('table');
const body = table.querySelector('tbody');

async function load() {
  status.textContent = 'Loading…';
  const response = await fetch('/api/stations');
  const { stations } = await response.json();

  body.replaceChildren(
    ...stations.map((station) => {
      const row = document.createElement('tr');
      for (const value of [station.name, station.latest, station.average]) {
        const cell = document.createElement('td');
        cell.textContent = value;
        row.append(cell);
      }
      return row;
    }),
  );
  table.hidden = false;
  status.textContent = `${stations.length} stations`;
}

button.addEventListener('click', () => {
  load().catch((error) => {
    status.textContent = `Could not load stations: ${error.message}`;
  });
});
