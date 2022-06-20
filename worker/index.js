const {Miniflare} = require("miniflare");
const http = require("http");
const WebSocket = require("ws").WebSocket
const fetch = require("node-fetch");
const fs = require("fs").promises;

const ORCH = process.env.ORCH || "127.0.0.1:5001";
const NAME = process.env.NAME || "worker.dune";
const ws = new WebSocket('ws://' + ORCH + '/ws/worker');

const BUCKET_ROOT = process.env.BUCKET_ROOT

async function fetchFile(key){
    return await fs.readFile(BUCKET_ROOT + "/" + key);
}

ws.on('open', function open() {
    ws.send(JSON.stringify({
        "type": "auth", "name":NAME
    }));
});

const workers = {};


ws.on('message', async function message(e) {
    const data = JSON.parse(e.toString());
    if (data.type === "deploy") {
        console.log("Deploy ", data.id)
        const env = {}
        for (const db of data.dbs) {
            const db_name = db.name.toUpperCase().replaceAll("-", "_")
            env[db_name] = {
                writeDataPoint: async (params) => {
                    const res = await fetch("http://" + ORCH + "/database", {
                        method: 'POST', // or 'PUT'
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            metadata: params.labels,
                            metrics: params.metrics,
                            db: db.id
                        }),
                    })
                }
            }
        }
        for (const bucket of data.buckets) {
            const bucket_name = bucket.name.toUpperCase().replaceAll("-", "_")
            env[bucket_name] = {
                get: async (key) => {
                    return await fetchFile(bucket.name + "/" + key)
                }
            }
        }
        const code = await fs.readFile(BUCKET_ROOT + "/" + data.id + ".js")

        const mf = new Miniflare({
            script: code, globals: {
                fetch: fetch,
                env: env
            }
        });
        workers[data.id] = mf
    }
});

const host = '0.0.0.0';
const port = 5555;

const requestListener = async function (req, res) {
    if (req.method == 'POST') {
        console.log('POST')
        var body = ''
        req.on('data', function(data) {
            body += data
        })
        req.on('end', async function() {
	    try{
		if (req.url.length >= 37) {
                    const key = req.url.substring(1, 37);
                    const worker = workers[key];
                    const resDispatch = await worker.dispatchFetch("http://localhost:8787/" + key, {
			headers: {"X-Message": "1"},
			method: "POST",
			body: body
                    });
		}
		res.writeHead(200);
		res.end("");
	    }catch(error){
		res.writeHead(500);
		res.end("");		
	    }	
        })
    } else {
        console.log('GET')
        if (req.url.length >= 37) {
            const key = req.url.substring(1, 37);
            const worker = workers[key];
            const resDispatch = await worker.dispatchFetch("http://localhost:8787/" + key, {
                headers: {"X-Message": "1"},
            });
            res.writeHead(200);
            res.end("My first server!");
        }
    }
};

const server = http.createServer(requestListener);
server.listen(port, host, () => {
    console.log(`Server is running on http://${host}:${port}`);
});
