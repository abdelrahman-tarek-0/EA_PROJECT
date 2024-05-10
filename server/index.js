const path = require('path')
const fs = require('fs')
const express = require('express')
const {Server} = require('socket.io')
const cors = require('cors')
const open = require('open')

const app = express()


app.use(cors())
app.use(express.json())
app.use(express.urlencoded({ extended: true }))
app.use(express.static(path.join(__dirname, 'public')))

let currentReports = []
let reports = {}

const server = require('http').createServer(app)

const io = new Server(server, {
   cors: {
      origin: '*',
      methods: ['GET', 'POST']
   }
})

io.on('connection', (socket) => {
      console.log('User connected')
      socket.on('disconnect', () => {
         console.log('User disconnected')
      })
})

app.get('/', (req, res) => {
   res.sendFile(path.join(__dirname, 'public', 'pages', 'main', 'index.html'))
})
app.get('/start', (req, res) => {
   res.sendFile(path.join(__dirname, 'public', 'pages', 'start', 'start.html'))
})
app.get('/reports', (req, res) => {
   res.sendFile(path.join(__dirname, 'public', 'pages', 'reports', 'reports.html'))
})
app.get('/model/:id', (req, res) => {
   const file = path.join(__dirname, 'public', 'pages', 'try-model', 'model.html')
   const html = fs.readFileSync(file, 'utf8')
   res.send(html.replaceAll('{{ID}}', req.params.id))
})

app.get('/health', (req, res) => {
   res.send("Ok")
})

app.get('/api/reports', (req, res) => {
   res.json(currentReports)
})
app.get('/api/reports/list', (req, res) => {
   const keys = Object.keys(reports)
   const data = keys.map(key => {
      return {
         id: key,
         timestamp: reports[key].timestamp,
      }
   })
   res.json(data)
})
app.get('/api/reports/:id', (req, res) => {
   const { id } = req.params
   res.json(reports[id])
})

app.post('/reports', (req, res) => {
   const data = req.body
   if (data?.command === 'start') {
      currentReports = [{
         ...data,
      }]
   } else if(data?.command === 'finish') {
      currentReports.push({
         ...data,
      })
      const id = data.id

      reports[id] = {
         data: currentReports,
         id: id,
         timestamp: Date.now(),
      }

      currentReports = []
   }
   else{
      currentReports.push(data)
   }
    io.emit('report', {
      ...data,
      reportsSaved: currentReports.length,
    })
    res.send('Report received')
})

server.listen(8001, () => {
   open('http://127.0.0.1:8001')
   console.log('Server is running on port http://127.0.0.1:8001')
})
