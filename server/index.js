const express = require('express')
const cors = require('cors')

const app = express()

app.use(cors())
app.use(express.json())
app.use(express.urlencoded({ extended: true }))

app.get('/', (req, res) => {
   res.send("Ok")
})

app.post('/reports', (req, res) => {
    console.log(req.body)
    res.send('Report received')
})

app.listen(8001, () => {
   console.log('Server is running on port http://localhost:8001')
})
