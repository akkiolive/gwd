var fs = require('fs');
var express = require("express")

console.log("hey")


app = express()

app.get("/*", (req, res) => {
    console.log(req)
    res.sendFile(__dirname + req.url)
})

app.listen(3000)



fs.readFile('/test.txt', 'utf8', function (err, data) {
    console.log(data);
})


fs.writeFileSync("text.txt","Hello")