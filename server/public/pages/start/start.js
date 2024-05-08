const form = document.querySelector('#start_form')
const modelUrl = 'http://127.0.0.1:8000'

const checkBackStatus = async () => {
   try {
      let res = await fetch(`${modelUrl}/status`)
      let data = await res.text()
      if (data === 'Running') {
         window.location.href = '/reports'
         return false
      }
      return true
   } catch (error) {
      window.location.href = '/'
      return false
   }
}

const startModel = async (data) => {
   try {
      fetch(`${modelUrl}/run/`, {
         method: 'POST',
         headers: {
            'Content-Type': 'application/json',
         },
         body: JSON.stringify(data),
      })

      window.location.href = '/reports'
   } catch (error) {
      window.location.href = '/'
   }
}

form.addEventListener('submit', async (e) => {
   e.preventDefault()
   const formData = new FormData(form)

   const keys = formData.keys()
   const values = formData.values()

   const data = {}

   for (const key of keys) {
      data[key] = Number(values.next().value)
   }

   if (!await checkBackStatus()) {
      return
   }
   startModel(data)
})
