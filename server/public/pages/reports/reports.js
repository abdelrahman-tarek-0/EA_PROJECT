const ulReports = document.getElementById('reports')
const modelUrl = 'http://127.0.0.1:8000'

const socket = io()

const checkBackStatus = async () => {
   try {
      let res = await fetch(`${modelUrl}/status`)
      let data = await res.text()
      if (data === 'Idle') {
         window.location.href = '/start'
         return false
      }
      return true
   } catch (error) {
      window.location.href = '/'
      return false
   }
}

const getReports = async () => {
   try {
      let res = await fetch(`/api/reports`)
      let data = await res.json()
      return data
   } catch (error) {
      return []
   }

}

checkBackStatus().then(async (status) => {
   if (!status) return
   
   const reports = await getReports()
   reports.forEach(report => {
      const li = document.createElement('li')
      li.textContent = JSON.stringify(report)
      ulReports.appendChild(li)
   })

   socket.on('connect', () => {
      console.log('Connected to server')
   })

   socket.on('report', (data) => {
      const li = document.createElement('li')
      li.textContent = JSON.stringify(data)
      ulReports.appendChild(li)
   })
})
