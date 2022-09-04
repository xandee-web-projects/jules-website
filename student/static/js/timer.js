setInterval(updateCountdown, 1000)
function updateCountdown(){
    let hrs = Math.floor(time/3600)
    let mins = Math.floor(time/60)
    let secs = Math.floor(time%60)
    secs = secs < 10 ? "0"+secs : secs
    mins = mins < 10 ? "0"+mins : mins
    hrs = hrs < 10 ? "0"+hrs : hrs
    
    document.getElementById("timer").innerHTML = `${hrs}:${mins}:${secs}`
    time --
}