const ulReports = document.getElementById('reports')
const populationSpace = document.getElementById('population_space')
const currentGeneration = document.getElementById('current_generation')
const modelUrl = 'http://127.0.0.1:8000'

const socket = io()
let reportsList = []

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

const notification = (message, duration=5000) => {
   Toastify({
      text: message,
      duration,
      newWindow: true,
      // close: true,
      gravity: 'top',
      position: 'right',
      // backgroundColor: 'linear-gradient(to right, #00b09b, #96c93d)',
      stopOnFocus: true,
      onClick: function () {},
   }).showToast()
}
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

const controller = async (data, delay) => {
   const li = document.createElement('li')
   li.textContent = JSON.stringify(data)
   ulReports.appendChild(li)

   const command = data?.command

   if (command === 'create_individual') {
      const individual = data?.individual
      notification(`New Individual Created: ${individual.id}`)

      const ind = document.createElement('div')
      const id = document.createElement('div')
      const fitness = document.createElement('div')
      const container = document.createElement('div')

      ind.innerHTML = choseRandomEmojiPerson()
      id.textContent = `${individual.id}`
      fitness.textContent = `${individual.fitness?.toFixed(3)}`

      ind.style.fontSize = '24px'
      fitness.style.fontSize = '12px'

      ind.style.marginBottom = '5px'
      id.style.marginBottom = '5px'
      fitness.style.marginBottom = '5px'

      container.appendChild(id)
      container.appendChild(ind)
      container.appendChild(fitness)

      // give it random location in the population space
      container.style.position = 'absolute'
      container.style.left = `${Math.random() * 100}%`
      container.style.top = `${Math.random() * 100}%`
      container.style.transform = 'translate(-50%, -50%)'
      container.style.display = 'flex'
      container.style.flexDirection = 'column'
      container.style.alignItems = 'center'
      container.style.cursor = 'pointer'
      container.addEventListener('click', () => {
         alert(JSON.stringify(individual.genes))
      })

      populationSpace.appendChild(container)
   } else if (command === 'generation_started') {
      const generation = data?.generation
      notification(
         `Generation started: ${generation} with Fitness: ${data.best_fitness}`,
         10000
      )

      currentGeneration.innerHTML = `
         Generation: ${generation}
         <br />
         <span style="font-size: 12px; font-weight: normal;">Best Fitness: ${data.best_fitness}</span>
      `
   }

   if (delay) await sleep(delay)
   return true
}

checkBackStatus().then(async (status) => {
   if (!status) return

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

      if(data?.reportsSaved !== reportsList.length){
         const notSavedReports = await getReports()
         reportsList = notSavedReports
      }

      reportsList.push(data)
      controller(data)
   })
})
