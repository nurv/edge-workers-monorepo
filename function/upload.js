const fs = require("fs").promises;

async function main(){
    const content = await fs.readFile(process.argv[2]);
    const res = await fetch("http://127.0.0.1:8000/function/6549eb0f-5d61-4848-8239-6d1a3883e974/submit", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            code: content.toString()
        }),
    }).catch((e) => {
        console.error(e)
    })
}

main().then(() => {
    console.log("Uploaded " + process.argv[2])
})