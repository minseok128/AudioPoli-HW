const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');

const app = express();

app.use(bodyParser.json({ limit: '50mb' }));
app.use(bodyParser.urlencoded({ limit: '50mb', extended: true }));

app.post('/rasberry', (req, res) => {
    const encodedAudio = req.body.sound;

    // Base64 문자열을 버퍼로 변환
    const audioBuffer = Buffer.from(encodedAudio, 'base64');

    // 파일로 저장
    fs.writeFile('output.wav', audioBuffer, (err) => {
        if (err) {
            console.error(err);
            res.status(500).send('Error saving the file');
        } else {
            res.send('File saved successfully');
        }
    });
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
