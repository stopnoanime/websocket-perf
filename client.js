const WebSocket = require('ws');
const { io } = require('socket.io-client');

const SERVER_TYPE = process.argv[2];

const SERVER_PORT = 8000;
const NUM_CLIENTS = 10;
const MESSAGE_COUNT = 1000;

console.log(`Starting ${NUM_CLIENTS} WebSocket clients connecting using ${SERVER_TYPE} to port ${SERVER_PORT}...`);

let totalMessages = 0;
let startTime, endTime;

for (let i = 0; i < NUM_CLIENTS; i++) {
    let socket;

    if (SERVER_TYPE == 'websocket') {
        socket = new WebSocket(`ws://localhost:${SERVER_PORT}`);

        socket.on('open', () => {
            console.log('WebSocket connection established!');
        });
    } else {
        socket = io(`http://localhost:${SERVER_PORT}`);

        socket.on('connect', () => {
            console.log('Socket.io connection established!');
        });
    }

    socket.on('message', (data) => {
        if (totalMessages === 0)
            startTime = Date.now();

        totalMessages++;
        endTime = Date.now();

        if (totalMessages === NUM_CLIENTS * MESSAGE_COUNT) {
            const elapsedTime = endTime - startTime;
            console.log(`Test completed in ${elapsedTime}ms`);
            socket.close();
        }
    });
}
