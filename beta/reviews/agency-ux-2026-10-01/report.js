const filters = [...document.querySelectorAll('[data-filter]')];
const findings = [...document.querySelectorAll('.finding')];
const status = document.querySelector('#filter-status');
filters.forEach(button => button.addEventListener('click', () => {
  const filter = button.dataset.filter;
  filters.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
  findings.forEach(item => { item.hidden = filter !== 'all' && !item.dataset.category.split(' ').includes(filter); });
  status.textContent = `Showing ${findings.filter(item => !item.hidden).length} of ${findings.length} findings.`;
}));
let openBeforePrint = [];
window.addEventListener('beforeprint', () => {
  openBeforePrint = [...document.querySelectorAll('details')].filter(item => item.open);
  document.querySelectorAll('details').forEach(item => { item.open = true; });
});
window.addEventListener('afterprint', () => {
  document.querySelectorAll('details').forEach(item => { item.open = openBeforePrint.includes(item); });
});
document.querySelector('#print-report').addEventListener('click', () => window.print());
