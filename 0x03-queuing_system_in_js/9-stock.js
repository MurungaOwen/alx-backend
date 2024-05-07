import express from 'express';
import redis from 'redis';
import { promisify } from 'util';

const app = express();

const client = redis.createClient();

const listProducts = [
    { id: 1, name: 'Suitcase 250', price: 50, stock: 4 },
    { id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
    { id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
    { id: 4, name: 'Suitcase 1050', price: 550, stock: 5 }
  ];

function getItemById(id) {
    const item = listProducts.find((val)=>val.id === id);
    if (item) {
        return item;
    } else {
        return "Not found";
    }
}

const getAsync = promisify(client.get).bind(client);


function reserveStockById(itemId, stock) {
    const stringItemId = itemId.toString()
    client.set(stringItemId, stock, redis.print);
  }

async function getCurrentReservedStockById(itemId) {
    const reply = await getAsync(itemId);
    return reply;
}

app.set('port', 1245);

app.listen(app.get('port'), () => {
    console.log("We live");
});

app.get('/list_products', (req, res) => {
    const new_response = []
    listProducts.forEach((val) => {
        new_response.push({
            "itemId": val.id,
            "itemName": val.name,
            "price": val.price,
            "initialAvailableQuantity": val.stock,
        });
    });
    res.status(200).send(new_response);
});

app.get('/list_products/:itemId', async (req, res) => {
    const itemId = Number(req.params.itemId);

    const item = getItemById(itemId);

    if (typeof(item) === 'object') {
        const [result] = await Promise.allSettled([getCurrentReservedStockById(itemId.toString())])
        const resp = {
            "itemId":item.id,
            "itemName":item.name,
            "price":item.price,
            "initialAvailableQuantity":item.stock,
            "currentQuantity": result.value
        }
        res.status(200).send(resp);
    } else {
        res.status(500).send({"status":"Product not found"})
    }
});

app.get('/reserve_product/:itemId', (req, res) => {
    const itemId = Number(req.params.itemId);

    const item = getItemById(itemId);

    if (typeof(item) === 'object') {
        if(item.stock >= 1) {
            reserveStockById(itemId, item.stock);
            res.status(200).send({"status":"Reservation confirmed","itemId":itemId});
        } else {
            res.status(500).send({"status":"Not enough stock available","itemId":itemId})
        }
    } else {
        res.status(500).send({"status":"Product not found"})
    }
})


module.exports = app
