const path = require('path')
const express = require('express')
const {Server} = require('socket.io')
const cors = require('cors')

const app = express()


app.use(cors())
app.use(express.json())
app.use(express.urlencoded({ extended: true }))
app.use(express.static(path.join(__dirname, 'public')))

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

app.get('/health', (req, res) => {
   res.send("Ok")
})

app.post('/reports', (req, res) => {
    io.emit('report', req.body) 
    res.send('Report received')
})

server.listen(8001, () => {
   console.log('Server is running on port http://127.0.0.1:8001')
})
