const form = document.querySelector('#start_form')
const addLayerBtn = document.querySelector('#add-layer')
const visualizeNNBtn = document.querySelector('#Visualize-NN-btn')
const visualizeNNSection = document.querySelector('#Visualize-NN-section')

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

const getModelInfo = async (layers) => {
   let res = await fetch(`${modelUrl}/modelInfo/`, {
      method: 'POST',
      headers: {
         'Content-Type': 'application/json',
      },
      body: JSON.stringify(layers),
   })

   let data = await res.json()

   return data
}

checkBackStatus()

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

addLayerBtn.addEventListener('click', () => {

   // <button type="button" class="remove-layer" onclick="deleteElement('layer-1')">Remove Layer</button>

   const layersInputs = document.querySelectorAll('.nn-layers')

   const section = document.querySelector('#nn-algorithm')
   const div = document.createElement('div')
   const h4 = document.createElement('h4')
   const divInput = document.createElement('div')
   const labelN = document.createElement('label')
   const inputN = document.createElement('input')
   const labelA = document.createElement('label')
   const select = document.createElement('select')
   const button = document.createElement('button')

   const layersCount = layersInputs.length + 1

   h4.textContent = `Layer ${layersCount}`
   divInput.classList.add('input-comp')
   labelN.setAttribute('for', `nn-layer-${layersCount}`)
   labelN.textContent = 'Number of neurons: '
   inputN.setAttribute('type', 'number')
   inputN.setAttribute('id', `nn-layer-${layersCount}`)
   inputN.setAttribute('name', `nn-layer-${layersCount}`)
   inputN.setAttribute('min', '1')
   inputN.setAttribute('required', '')
   inputN.setAttribute('value', '8')
   inputN.classList.add('nn-layers')

   button.setAttribute('type', 'button')
   button.classList.add('remove-layer')
   button.textContent = 'Remove Layer'
   button.setAttribute('onclick', `deleteElement('layer-${layersCount}')`)

   div.id = `layer-${layersCount}`

   labelA.setAttribute('for', `nn-activation-${layersCount}`)
   labelA.textContent = 'Activation Function: '
   select.setAttribute('name', `nn-activation-${layersCount}`)
   select.setAttribute('id', `nn-activation-${layersCount}`)
   select.innerHTML = `
      <option value="relu">ReLU</option>
      <option value="sigmoid">Sigmoid</option>
      <option value="tanh">Tanh</option>
      <option value="linear">Linear</option>
   `

   divInput.appendChild(labelN)
   divInput.appendChild(inputN)
   divInput.appendChild(labelA)
   divInput.appendChild(select)
   divInput.appendChild(button)

   div.appendChild(h4)
   div.appendChild(divInput)


   section.insertBefore(div, addLayerBtn)
})

visualizeNNBtn.addEventListener('click', async () => {
   const layersInputs = document.querySelectorAll('.nn-layers').length

   const layers = []

   for (let i = 1; i <= layersInputs; i++) {
      layers.push({
         n: Number(document.querySelector(`#nn-layer-${i}`).value),
         activation: document.querySelector(`#nn-activation-${i}`).value,
      })
   }

   if (!layers.length) {
      alert('Please add layers to visualize the Neural Network')
      return
   }

   console.log(layers)

   getModelInfo({
      layers: layers,
   }).then((data) => {
      const image = data.image
      const numberOfWeights = data.weights

      visualizeNNSection.innerHTML = `
         <p>The length of the individual DNA: ${numberOfWeights} (NN weights + learning rate)</p>
         <img src="${image}" alt="Neural Network"/>
      `
   })
})

form.addEventListener('submit', async (e) => {
   e.preventDefault()
   const formData = new FormData(form)

   const editAlgorithm = {
      num_individuals: Number(formData.get('num_individuals')),
      num_generations: Number(formData.get('num_generations')),
      epochs: Number(formData.get('epochs')),
      mutateWeight: Number(formData.get('mutateWeight')),
      crossoverRate: Number(formData.get('crossoverRate')),
      delay: Number(formData.get('delay')),
   }

   const layersInputs = document.querySelectorAll('.nn-layers').length

   const layers = []

   for (let i = 1; i <= layersInputs; i++) {
      layers.push({
         n: Number(formData.get(`nn-layer-${i}`)),
         activation: formData.get(`nn-activation-${i}`),
      })
   }
   if (!layers.length) {
      alert('Please add layers to start the Neural Network')
      return
   }

   editAlgorithm.layers = layers

   console.log(editAlgorithm)

   // getModelInfo({
   //    layers: editAlgorithm.layers,
   // }).then((data) => {
   //    console.log(data)
   // })


   if (!await checkBackStatus()) {
      return
   }
   startModel(editAlgorithm)

   // console.log(formData.get('nn-layer-1'))
   // console.log(formData.get('nn-activation-1'))

   // const keys = formData.keys()
   // const values = formData.values()

   // console.log(keys)
   // console.log(values)

   // const data = {}

   // for (const key of keys) {
   //    console.log(key, values.next().value)
   //    // if(isNaN(Number(values.next().value))) {
   //    //    data[key] = values.next().value
   //    // }else{
   //    //    data[key] = Number(values.next().value)
   //    // }

   //    data[key] = Number(values.next().value)

   // }

   // console.log(data)

})
