const { createServer } = require('http');
const { Server } = require('socket.io');

const PORT = 8000;
const EXPECTED_CLIENTS = 50;
const MESSAGE_COUNT = 100;

const httpServer = createServer();
const io = new Server(httpServer);

let connectedClients = 0;
let startTime;

console.log(`Socket.io server starting on port ${PORT}`);
console.log(`Waiting for ${EXPECTED_CLIENTS} clients to connect...`);

io.on('connection', (socket) => {
    connectedClients++;
    console.log(`Client connected (${connectedClients}/${EXPECTED_CLIENTS})`);

    socket.on('disconnect', () => {
        connectedClients--;

        if (connectedClients === 0) 
            process.exit(0);
    });

    if (connectedClients === EXPECTED_CLIENTS) {
        console.log('All clients connected. Starting test...');
        startTime = Date.now();

        for (let i = 0; i < MESSAGE_COUNT; i++) {
            io.emit("message", "test-payload");
        }

        const endTime = Date.now();
        console.log(`Test completed in ${endTime - startTime}ms`);
        console.log(`Sent ${MESSAGE_COUNT} messages to ${EXPECTED_CLIENTS} clients`);
    }
});

httpServer.listen(PORT);