var app = (function(o, $) {

    const self = this;

    o.main = {

        onHcaptchaSubmit: function onHcaptchaSubmit(token) {
            $("#id_captcha_response").val(token);
            $("form").submit();
        },

        getCookie: function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        },

        setupAjax: function setUpAjax() {
            const csrfToken = this.getCookie('csrftoken');
            $.ajaxSetup({
                beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrfToken);
                xhr.setRequestHeader("Accept", 'application/json');
                }
            });
        },

        temporaryDisable: function ($elem, timeout = 3000) {
            $elem.attr("disabled", true);
            setTimeout(() => {
                $elem.attr("disabled", false);
            }, timeout);
        },

        init: function initMain() {
            window.onHcaptchaSubmit = this.onHcaptchaSubmit;
        },

    }

    return o;
})(app || {}, jQuery);
