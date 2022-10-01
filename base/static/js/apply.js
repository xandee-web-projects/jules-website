$(document).ready(function () {
    
    var public_key = "pk_test_ad97943388f7189f0da4865d549f055ab89c44bc"
    const form = document.getElementById("form")
    
    form.addEventListener("submit", (event) => {
        event.preventDefault();
        var handler = PaystackPop.setup({
            key: public_key,
            email: document.getElementById('email').value,
            amount: parseInt(document.getElementById('amount').value) * 100,
            currency: 'NGN',
            callback: function(response) {
              var reference = response.reference;
              alert('Payment complete! Reference: ' + reference);
              // Make an AJAX call to your server with the reference to verify the transaction
            },
            onClose: function() {
              alert('Transaction was not completed, window closed.');
            },
          });
          handler.openIframe();
    })
});
