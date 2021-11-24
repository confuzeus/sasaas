var app = (function (o, $) {

    o.paddle = {
        closeCallback: function paddleCloseCallback() {
            const paymentCancelledToast = document.getElementById('paymentCancelledToast')
            const toast = new bootstrap.Toast(paymentCancelledToast);
            toast.show()
        },
        successCallback: function paddleSuccessCallback() {
            const currentUrl = window.location.href;
            window.location.href = currentUrl + "?success=True"
        },
        init: function paddleInit() {
            const $jsPaddleButton = $(".js-paddle-button");
            $jsPaddleButton.on("click", function () {
                const $this = $(this);
                const productId = parseInt($this.data("product"));
                const email = $this.data("email");
                const country = $this.data("country");
                o.main.temporaryDisable($this);
                Paddle.Checkout.open({
                    product: productId,
                    email: email,
                    country: country,
                    marketingConsent: "1",
                });
            });

            window.paddleCloseCallback = this.closeCallback;
            window.paddleSuccessCallback = this.successCallback;
        }
    }

    return o;

})(app || {}, jQuery);