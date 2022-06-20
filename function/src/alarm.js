export async function triggerAlarm() {
    await fetch("http://ix.dune:7000/on", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    });
}

export async function resetAlarm() {
    await fetch("http://ix.dune:7000/off", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    });
}