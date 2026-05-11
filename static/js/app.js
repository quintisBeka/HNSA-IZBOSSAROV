const el=document.getElementById('scanChart');
if(el){fetch('/api/analytics').then(r=>r.json()).then(d=>new Chart(el,{type:'line',data:{labels:d.labels,datasets:[{label:'Open Ports',data:d.values,borderColor:'#60a5fa'}]}}));}
