const modelId = document.querySelector('#modelId').dataset.id
const form = document.querySelector('#modelForm')
const results = document.querySelector('#result')
const modelUrl = 'http://127.0.0.1:8000'

let urlPath = window.location.pathname; 
let pathParts = urlPath.split('/');
let dataset = pathParts[pathParts.length - 2]; 


const checkModel = async () => {
   try {
      console.log(modelId, dataset)

      let res = await fetch(`${modelUrl}/model-status/?id=${modelId}&dataset=${dataset}`)
      let data = await res.json()
      console.log(data)
      if (!data.exists) {
         window.location.href = '/'
         return false
      }
      return true
   } catch (error) {
      window.location.href = '/'
      return false
   }
}

const predict = async (data) => {
   try {


      let res = await fetch(`${modelUrl}/predict/`, {
         method: 'POST',
         headers: {
            'Content-Type': 'application/json',
         },
         body: JSON.stringify(data),
      })

      let result = await res.json()
      return result.prediction
   } catch (error) {
      console.log(error)
      window.location.href = '/'
   }
}

checkModel().then()

form.addEventListener('submit', async (e) => {
   e.preventDefault()
   results.style.display = 'none'
   const formData = new FormData(form)
   const data = {
      id: modelId,
      dataset: dataset,
      data: [
         Number(formData.get('Age')),
         Number(formData.get('Year')),
         Number(formData.get('Nodes')),
      ],
   }

   console.log(data)

   const prediction = Number(await predict(data))




   const resultsTextEl = document.querySelector('#result-text')
   console.log(resultsTextEl)

   resultsTextEl.innerHTML = prediction > 0.5
      ? `
      <p style="color: red;">Is likely dead</p>
    `
      : `
      <p style="color: blue;">Is likely alive</p>
    `
   results.style.display = 'block'
})
