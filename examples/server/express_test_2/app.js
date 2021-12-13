// from https://expressjs.com/en/starter/hello-world.html

const express = require('express')
const app = express()
const port = 3000

app.get('/', (req, res) => {
  //res.send('Hello World!')

  // https://expressjs.com/en/4x/api.html#res.json
  res.json({ hello: 'world' })
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})

// Docker container exit handler
// https://github.com/nodejs/node/issues/4182
process.on('SIGINT', function() {
    process.exit();
});