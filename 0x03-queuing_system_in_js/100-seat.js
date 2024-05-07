import redis from 'redis';
import { createQueue } from 'kue';
import { promisify } from 'util';
import express from 'express';

const app = express();

const redisClient = redis.createClient();

const queue = createQueue();

let reservationEnabled = true; // make false when no seat available

function reserveSeat(number) {
    redisClient.set("available_seats", number);
}

const asyncGet = promisify(redisClient.get).bind(redisClient)

async function getCurrentAvailableSeats() {
    // return current available seats
    const value = await asyncGet("available_seats");
    return value
}

app.set("port", 1245);

app.listen(app.get("port"), () => {
    console.log("We are live code ninja");
    reserveSeat(50);
});

app.get('/available_seats', async (req, res) => {
    // returns number of available seats
    const [availableSeats] = await Promise.allSettled([getCurrentAvailableSeats()]);
    res.status(200).send({ "numberOfAvailableSeats" : availableSeats.value });
});

app.get('/reserve_seat', (req, res) => {
    if (!reservationEnabled) {
        res.status(400).send({ "status": "Reservation are blocked" });
    } else {
        const job = queue.create('reserve_seat').save((err) => {
            if (!err) {
                const msg = { "status": "Reservation in process" };
                res.status(200).send(msg);
            } else {
                const msg = { "status": "Reservation failed" };
                res.status(500).send(msg);
            }
        });

        job.on('complete', () => {
            console.log(`Seat reservation job ${job.id} completed`);
        });

        job.on('failed', (err) => {
            console.log(`Seat reservation job ${job.id} failed: ${err}`);
        });
    }
});

app.get('/process', (req, res) => {
    queue.process('reserve_seat', async (job, done) => {
        const [seats] = await Promise.allSettled([getCurrentAvailableSeats()]);
        // reserve a seat and decrement total seats by 1
        const seatValues = Number(seats.value)
        reserveSeat( seatValues - 1 );

        const [newAvailable] = await Promise.allSettled([getCurrentAvailableSeats]);
        const newAvailableSeats = Number(newAvailable.value);

        if (newAvailableSeats > -1) {
            done();
        } else {
            done(new Error("Not enough seats available"));
        }
        // if new seats are 0 then no more reservations
        if (newAvailableSeats <= 0) {
            reservationEnabled = false;
        }
    });
    const msg = { "status": "Queue processing" }
    res.status(200).send(msg);
})
