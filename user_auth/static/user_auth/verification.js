const phone_verification_url = "http://127.0.0.1:8000/api/verify/"

$(document).ready(() => {
    axios.defaults.xsrfCookieName = 'csrftoken'
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
    $("#verification").submit((event) => {
        console.log(type)
        event.preventDefault()
        let phone_code = $("#phone-verify-code").val()
        let email_code = $("#email-verify-code").val()

        console.log(phone_code, email_code)
        axios.post(phone_verification_url, {phone_code, email_code, type})
        .then(res => {
            console.log(res)
            window.location.href = `http://127.0.0.1:8000/home/`
        })
        .catch(err => console.log(err))
    })

})