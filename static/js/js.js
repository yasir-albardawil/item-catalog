var currentYear = new Date().getFullYear(),
	min = 1900,
	max = currentYear + 2,
	select = document.getElementById('year');

for (var i = min; i <= max; i++) {
	var opt = document.createElement('option');
	opt.value = i;
	opt.innerHTML = i;
	select.appendChild(opt);
}

