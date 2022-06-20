import {BucketModelLoader, EdgeModel} from "./edgeModel";
import {resetAlarm, triggerAlarm} from "./alarm";

const WINDOW = []
var MODEL = null;
var ANOMALLY = false;

async function handleRequest(request){
    try{
        var messages = await request.json();
        for (var msg of messages) {
            var payload = JSON.parse(msg.payload);
            await env.WEATHER.writeDataPoint({
                labels: ["Lisbon", "HomeLab", "DHT11"],
                metrics: [payload.temp, payload.hum]
            });
            if (WINDOW.length == 20){
                const res = await MODEL.predict(WINDOW)
                const sigma3 = res + (MODEL.std * 3);
                if(sigma3 < payload.temp && !ANOMALLY){
                    ANOMALLY = true;
                    await triggerAlarm();
                } else if(sigma3 > payload.temp && ANOMALLY){
                    ANOMALLY = false;
                    await resetAlarm();
                }
            }
            const length = WINDOW.push(payload.temp);
            if(length > 20){
                WINDOW.shift();
            }
            console.log(WINDOW);
        }

        return new Response(JSON.stringify(messages), { status: 200 });
    }catch(e){
        console.error(e);
    }
}

EdgeModel.loadModel(new BucketModelLoader(env.HOMELAB_TEMP_MODEL, "65019860-d4da-4e41-ba1e-df22d9543ed9")).then(async (model) => {
    MODEL = model;
    addEventListener("fetch", (event) => {
        event.respondWith(handleRequest(event.request));
    });
})
