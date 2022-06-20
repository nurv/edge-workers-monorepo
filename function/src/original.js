async function handleRequest(request){
    try{
        var messages = await request.json();

        for (var msg of messages) {
            var payload = JSON.parse(msg.payload);
            console.log(payload)
            await env.WEATHER.writeDataPoint({
                labels: ["Lisbon", "HomeLab", "DHT11"],
                metrics: [payload.temp, payload.hum]
            });
        }

        return new Response(JSON.stringify(messages), { status: 200 });
    }catch(e){
        console.error(e);
    }
}

addEventListener("fetch", (event) => {
    event.respondWith(handleRequest(event.request));
});