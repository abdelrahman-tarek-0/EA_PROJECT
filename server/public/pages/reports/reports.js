const ulReports = document.getElementById('reports')
const populationSpace = document.getElementById('population_space')
const currentGeneration = document.getElementById('current_generation')
const modelUrl = 'http://127.0.0.1:8000'


const loader = `<div class="lds-ring"><div></div><div></div><div></div><div></div></div>`

const socket = io()

let reportsList = []
const randomIfNotMet = (value, min, max) => {
   const random = Math.random() * value
   if (random > min && random < max) return random
   return randomIfNotMet(value, min, max)
}

function removeFadeOut(el, speed) {
   var seconds = speed / 1000
   el.style.transition = 'opacity ' + seconds + 's ease'

   el.style.opacity = 0
   setTimeout(function () {
      el?.parentNode?.removeChild(el)
   }, speed)
}

const move = (id, to, opts) => {
   const container = document.getElementById(id)
   const toContainer = document.getElementById(to)

   if (!container || !toContainer) return

   container.style.position = opts?.pos || 'static'
   const rect = container.getBoundingClientRect()
   const offsetX = rect.left - toContainer.getBoundingClientRect().left
   const offsetY = rect.top - toContainer.getBoundingClientRect().top
   container.style.transform = `translate(${offsetX}px, ${offsetY}px)`

   container.style.top = 0
   container.style.left = 0

   toContainer.appendChild(container)
   setTimeout(function () {
      container.style.transform = 'none'

      if (to !== 'population_space') return

      // let randomTop = Math.random() * 100
      // let randomLeft = Math.random() * 100

      // if (randomTop < 10) randomTop = 10
      // if (randomTop > 90) randomTop = 90

      // if (randomLeft < 5) randomLeft = 5
      // if (randomLeft > 95) randomLeft = 95

      let randomTop = randomIfNotMet(100, 10, 90)
      let randomLeft = randomIfNotMet(100, 5, 95)

      container.style.left = `${randomLeft}%`
      container.style.top = `${randomTop}%`

      // container.style.top = `${Math.random() * 100}%`
      // container.style.left = `${Math.random() * 100}%`
   }, 100)
}

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
      console.error(error)
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
const choseRandomEmojiPerson = () => {
   const emojis = [
      '<i class="fa-solid fa-person fa-xl"></i>',
      '<i class="fa-regular fa-person fa-xl"></i>',
      '<i class="fa-duotone fa-person fa-xl"></i>',
      '<i class="fa-solid fa-person-dress fa-xl"></i>',
      '<i class="fa-regular fa-person-dress fa-xl"></i>',
      '<i class="fa-duotone fa-person-dress fa-xl"></i>',
   ]
   return emojis[Math.floor(Math.random() * emojis.length)]
}

const notification = (message, duration = 5000) => {
   Toastify({
      text: message,
      duration,
      newWindow: true,
      // close: true,
      gravity: 'bottom',
      position: 'right',
      // backgroundColor: 'linear-gradient(to right, #00b09b, #96c93d)',
      stopOnFocus: true,
      onClick: function () {},
   }).showToast()
}

const popupGenes = (id) =>{
   const genes = JSON.parse(document.getElementById(id).dataset.genes)
   const genesView = genes.slice(0, 10)
   const learningRate = genes.at(-1)

   const htmlView = `
      <div style="display: flex; justify-content: space-between;">
         <div>Learning Rate</div>
         <div>${learningRate}</div>
      </div>

      <div style="display: flex; justify-content: space-between;">
         <div>Genes</div>
      </div>

      <div style="display: flex; justify-content: space-between; flex-direction: row;">
         ${genesView.map(gene => `<div> ${gene} </div>`).join('')}
      </div>
   `

   Swal.fire({
      title: 'Genes',
      html: htmlView,
      showCloseButton: true,
      showConfirmButton: false,
   })
   // alert(genes)
}

// {"command":"finish","id":1715355693753,"fitness":0.7207792401313782,"reportsSaved":0}
const popupEndAlgorithm = (data) => {
   // Swal.fire({
   //    title: `"Training ${data.id} is done with accuracy: ${data.fitness}"`,
   //    showDenyButton: true,
   //    confirmButtonText: "Try Model",
   //    denyButtonText: `Download Model`,
   //  }).then((result) => {
   //    if (result.isConfirmed) {
   //       window.open(`/model/${data.id}`, '_blank')
   //    } else if (result.isDenied) {
        
   //    }
   //  });

   const imageOV = `/uploads/${data.id}-history-ov.png`
   const imageB = `/uploads/${data.id}-history-b.png`
   const modelLink = `/uploads/${data.id}.keras`

   Swal.fire({
      title: `Training is done`,
      // icon: "info",
      html: `
      <style>
      button {
          display: block;
          width: 100%;
          text-align: center;
          padding: 10px 20px;
          border: none;
          border-radius: 5px;
          background-color: #007BFF;
          color: #fff;
          cursor: pointer;
          margin: 10px 0;
      }
  
      #cont-btn {
          display: flex;
          flex-direction: column;
      }
  
      button:hover {
          background-color: #0056b3;
      }
  
      #container {
          padding: 20px;
          border-radius: 10px;
          background-color: #f8f9fa;
          margin: auto;
          box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
          width: 300px;
          display: flex;
          flex-direction: column;
          align-items: center;
      }
  
      .section {
          display: flex;
          flex-direction: column;
          align-items: flex-start;
          width: 100%;
          margin-bottom: 10px;
      }
  
      .images {
          display: flex;
          flex-direction: column;
          align-items: center;
      }
  
      .images img {
          width: 600px;
          height: 400px;
          margin-bottom: 10px;
      }
  </style>
  
  <div id="container">
      <div class="section">
          <div>Model ID</div>
          <div>${data.id}</div>
      </div>
      <div class="section">
          <div>Accuracy</div>
          <div>${data.fitness}</div>
      </div>
  
      <div class="section">
          <div>Model History</div>
          <div class="images">
              <img src="${imageOV}" />
              <img src="${imageB}" />
          </div>
      </div>
  
      <div class="section">
          <div>Options</div>
          <div id="cont-btn">
              <button onclick="window.open('/model/${data.dataset}/${data.id}', '_blank')">Try Model</button>
              <button style="background-color: red;" onclick="window.open('${modelLink}', '_blank')">Download Model</button>
          </div>
      </div>
  </div>
      `,
      showCloseButton: false,
      showCancelButton: false,
      showConfirmButton: false,
      customClass: 'swal-wide',
    });
}

const createIndividual = (individual, opt) => {
   const ind = document.createElement('div')
   const id = document.createElement('div')
   const fitness = document.createElement('div')
   const container = document.createElement('div')

   container.id = `ind-${individual.id}`
   container.classList.add(opt?.new ? 'new-individual' : 'individual')

   ind.innerHTML = choseRandomEmojiPerson()
   id.textContent = `${individual.id}`
   fitness.textContent = `${
      typeof individual.fitness === 'number'
         ? individual.fitness.toFixed(3)
         : individual.fitness
   }`

   ind.style.fontSize = '24px'
   fitness.style.fontSize = '12px'

   ind.style.marginBottom = '5px'
   id.style.marginBottom = '5px'
   fitness.style.marginBottom = '5px'

   container.appendChild(id)
   container.appendChild(ind)
   container.appendChild(fitness)

   // give it random location in the population space
   container.style.position = opt?.pos || 'absolute'
   container.style.left = `${Math.random() * 100}%`
   container.style.top = `${Math.random() * 100}%`
   container.style.transform = !opt?.noTrans ? 'translate(-50%, -50%)' : 'none'
   container.style.display = 'flex'
   container.style.flexDirection = 'column'
   container.style.alignItems = 'center'
   container.style.cursor = 'pointer'
   container.style.transition = 'all 0.5s ease'
   // container.addEventListener('click', () => {
   //    alert(JSON.stringify(individual.genes))
   // })
   container.dataset.genes = JSON.stringify(individual.genes)
   container.addEventListener('click', () => {
      popupGenes(container.id)
   })

   // populationSpace.appendChild(container)
   if (opt?.to) {
      document.getElementById(opt.to).appendChild(container)
   } else {
      populationSpace.appendChild(container)
   }
}

const editIndividual = (indId, individual) => {
   const container = document?.getElementById(`ind-${indId}`)
   const fitness = container?.querySelector('div:nth-child(3)')
   const id = container?.querySelector('div:nth-child(1)')
   fitness.innerHTML = `${
      typeof individual?.fitness === 'number'
         ? individual?.fitness.toFixed(3)
         : individual?.fitness
   }`
   if (individual?.id) {
      id.textContent = `${individual.id}`
      container.id = `ind-${individual.id}`
   }
}

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

const controller = async (data, delay = 500) => {
   // const li = document.createElement('li')
   // li.textContent = JSON.stringify(data)
   // ulReports.appendChild(li)

   const command = data?.command

   if (command === 'create_individual') {

      createIndividual(data.individual, {
         pos: 'absolute',
      })
      // notification(`New Individual Created: ${data.individual.id}`)
   } else if (command === 'generation_started') {
      const generation = data?.generation
      notification(
         `Generation started: ${generation} with Fitness: ${data?.best_fitness}`,
         10000
      )

      currentGeneration.innerHTML = `
         Generation: ${generation}
         <br />
         <span style="font-size: 12px; font-weight: normal;">Best Fitness: ${data?.best_fitness}</span>
      `
   } else if (command === 'selection') {
      const target = data?.target
      const r1 = data?.r1
      const r2 = data?.r2
      const r3 = data?.r3

      // notification(`Selected target: ${target.id}`, 5000)

      move(`ind-${target.id}`, `selected-target`)
      move(`ind-${r1.id}`, `selected`)
      move(`ind-${r2.id}`, `selected`)
      move(`ind-${r3.id}`, `selected`)
   } else if (command === 'mutation') {
      const mutated = document.getElementById(`ind-mutated`)
      if (mutated) {
         document.querySelectorAll('#ind-mutated').forEach((el) => {
            removeFadeOut(el, 500)
         })
      }

      const r1 = data?.r1
      const r2 = data?.r2
      const r3 = data?.r3

      move(`ind-${r1.id}`, `mutation-operation-1`)
      move(`ind-${r2.id}`, `mutation-operation-2`)
      move(`ind-${r3.id}`, `mutation-operation-3`)

      if (delay) {
         await sleep(delay)
      }

      createIndividual(
         {
            id: 'mutated',
            genes: data?.mutated?.genes,
            fitness: data?.mutated?.fitness,
         },
         {
            pos: 'static',
            to: 'mutation-operation-4',
            noTrans: true,
         }
      )

      // document.querySelector('body').appendChild(ind)

      // move(`ind-mutated`, `mutation-operation-4`)
   } else if (command === 'crossover') {
      const crossovered = document.getElementById(`ind-mutated`)
      if (crossovered) {
         document.querySelectorAll('#ind-trail').forEach((el) => {
            removeFadeOut(el, 500)
         })
      }

      const target = data?.target

      move(`ind-${target.id}`, `crossover-operation-1`)
      move(`ind-mutated`, `crossover-operation-2`)

      if (delay) {
         await sleep(delay)
      }

      createIndividual(
         {
            id: 'trail',
            genes: data?.trail,
            fitness: 0,
         },
         {
            pos: 'static',
            to: 'crossover-operation-3',
            noTrans: true,
         }
      )

      // move(`ind-trail`, `crossover-operation-3`)
   } else if (command === 'survive-started') {
      const target = data?.target
      move(`ind-${target?.id}`, `survival-operation-1`)
      move(`ind-trail`, `survival-operation-2`)
      editIndividual('trail', {
         fitness: loader,
      })
   } else if (command === 'survive-trail_gene_fitness') {
      const mutated = document.getElementById(`ind-mutated`)
      if (mutated) {
         document.querySelectorAll('#ind-mutated').forEach((el) => {
            removeFadeOut(el, 500)
         })
      }

      const fitness = data?.fitness
      editIndividual('trail', {
         fitness,
      })
   } else if (command === 'survive-finished') {
      const winner = data?.winner
      const new_individual = data?.new_individual
      console.log(data)
      if (winner === 'trail_gene') {
         notification(`Trail Gene won with fitness: ${new_individual?.fitness}`)
         move(`ind-trail`, `survival-operation-3`)
      } else {
         notification(`Target won with fitness: ${new_individual?.fitness}`)
         move(`ind-${new_individual?.id}`, `survival-operation-3`)
      }
   } else if (command === 'new-individual') {
      const individual = data?.individual
      // notification(`New Individual Created: ${individual.id}`)

      createIndividual(
         {
            id: `new-${individual.id}`,
            fitness: individual.fitness,
            genes: individual.genes,
         },
         {
            pos: 'static',
            to: 'new-bus',
            noTrans: true,
            new: true,
         }
      )
   } else if (command === 'generation_finished') {
      const individuals = document.querySelectorAll('.individual')
      individuals.forEach((el, i) => {
         removeFadeOut(el, 500 + i * 50)
      })

      await sleep(500 + individuals.length * 50 + 100)
      const newIndividuals = document.querySelectorAll('.new-individual')
      newIndividuals.forEach((el, i) => {
         editIndividual(`new-${el.id.split('-')[2]}`, {
            id: `${i}`,
            fitness: el.querySelector('div:nth-child(3)').textContent,
            genes: JSON.parse(el.dataset.genes),
         })

         el.classList.remove('new-individual')
         el.classList.add('individual')
      })

      const moveInds = document.querySelectorAll('.individual')
      moveInds.forEach((el, i) => {
         console.log(`Moving ${i} to population_space`)
         move(`ind-${i}`, 'population_space', {
            pos: 'absolute',
         })
      })
   } else if (command === 'clean_up') {
      const inds = data?.data
      for (let i = 0; i < inds?.length; i++) {
         const ind = inds[i]
         move(`ind-${ind?.id}`, `population_space`, {
            pos: 'absolute',
         })
      }

      if (data.deleteTrail) {
         const crossovered = document.getElementById(`ind-trail`)
         if (crossovered) {
            document.querySelectorAll('#ind-trail').forEach((el) => {
               removeFadeOut(el, 500)
            })
         }
      }

      if (data.deleteMutated) {
         const mutated = document.getElementById(`ind-mutated`)
         if (mutated) {
            document.querySelectorAll('#ind-mutated').forEach((el) => {
               removeFadeOut(el, 500)
            })
         }
      }
   } else if (command === 'finish') {
      popupEndAlgorithm(data)
   }

   if (delay) await sleep(delay)
   return true
}

checkBackStatus().then(async (status) => {
   // if (!status) return

   const reports = await getReports()
   reportsList = reports

   for (let i = 0; i < reports.length; i++) {
      const report = reports[i]
      await controller(report, 0)
   }

   socket.on('connect', () => {
      console.log('Connected to server')
   })

   socket.on('report', async (data) => {
      if (data?.reportsSaved !== reportsList.length) {
         const notSavedReports = await getReports()
         reportsList = notSavedReports
      }

      reportsList.push(data)
      await controller(data)
   })
})
