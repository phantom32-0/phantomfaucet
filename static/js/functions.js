// phantoms duinocoin faucet
// why are you looking here

function faucetactivate() {
    var serverresponse
    var ducoUsername = document.getElementById("usernameduco").value; 
    alert("trying to request ducos amogus")
    thebutton = document.getElementById("gibducos")
    document.getElementById("usernameduco").disabled = true
    
    thebutton.classList.add("is-loading")

    fetch('/faucetchungus?username='+ducoUsername, {method: 'POST'})
    .then(function(response){
        if (response.status == 200){
            console.log("received 200 yay removing loading baner")
            thebutton.disabled = true
            thebutton.classList.remove("is-loading", "is-duco-alt", "is-primary")
            thebutton.classList.add("is-success")
        }
        else if (response.status == 429){
            alert("looks like you are sending a lot of requests! calm down")
        }
        else{
            console.log("did not receive 200 instead received " + response.status + " making the buton red")
            thebutton.disabled = true
            thebutton.classList.remove("is-loading", "is-duco-alt", "is-primary")
            thebutton.classList.add("is-danger")
        }
        return response.text();
    })
    .then(function(data) {
        alert(data)
    })
}