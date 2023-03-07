const item_cards = document.getElementById("item_cards")


function run_confetti(){
    var duration = 10 * 1000;
    var end = Date.now() + duration;
    
    (function frame() {
      // launch a few confetti from the left edge
      confetti({
        particleCount: 7,
        angle: 60,
        spread: 55,
        origin: { x: 0 }
      });
      // and launch a few from the right edge
      confetti({
        particleCount: 7,
        angle: 120,
        spread: 55,
        origin: { x: 1 }
      });
    
      // keep going until we are out of time
      if (Date.now() < end) {
        requestAnimationFrame(frame);
      }
    }());
}


function get_all_items() {
    item_cards.innerHTML = "Please wait while we create our brand new jewelry. Give us a few more seconds. ..."
    url = '/api/items'
    fetch(url)
        .then(recordset => recordset.json())
        .then(result => {
            item_cards.innerHTML = ""
            result.forEach(function (r) {
                item_cards.innerHTML += "<div class='col'>" +
                    "<div class='card shadow-sm'>" +
                    "<img class='card-img-top' src='" + r.thumbnail + "'alt='Product Image'>" +
                    "<div class='card-body'>" +
                    "<p class='card-text name'>" + r.name + "</p>" +
                    "<p class='card-text'>" + r.description + "</p>" +
                    "<div class='d-flex justify-content-between align-items-center'>" +
                    "<div class='btn-group'>" +
                    "<button type='button' onclick='order_item(" + r.item_id + ")' class='btn btn-sm btn-success' data-product-id='" + r.item_id + "'>Order now</button>" +
                    "</div>" +
                    "<small class='text-muted'>" + r.stock + " available</small>" +
                    "</div></div></div></div>"
            });
        });
}


function order_item(item_id) {
    
    url = '/api/items/' + item_id
    fetch(url, {
        method: "PATCH",
    })
        .then((response) => response.json())
        .then((result) => {
            console.log(result);
        })
        run_confetti();
        get_all_items();
}


document.addEventListener("DOMContentLoaded", () => {
    get_all_items();
});
