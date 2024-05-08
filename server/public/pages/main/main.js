const statusEl = document.getElementById('status')
const modelUrl = 'http://127.0.0.1:8000'
fetch(`${modelUrl}/status`)
   .then((res) => res.text())
   .then((data) => {
      if (data === 'Idle') {
         window.location.href = '/start'
      } else if (data === 'Running') {
         window.location.href = '/reports'
      }
   })
   .catch((err) => {
      statusEl.textContent = 'Model server is not running'
      // change color to red
      statusEl.style.color = 'red'
   })
