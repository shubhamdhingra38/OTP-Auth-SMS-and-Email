const auth_url = "http://127.0.0.1:8000/api/auth/"


//https://stackoverflow.com/questions/1184624/convert-form-data-to-javascript-object-with-jquery
function objectifyForm(formArray) {
    //serialize data function
    var returnArray = {};
    console.log(formArray.length)
    for (var i = 0; i < formArray.length; i++){
        returnArray[formArray[i]['name']] = formArray[i]['value'];
    }
    return returnArray;
}


axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"


$(document).ready(() => {


    $('#register').submit((event) => {
            event.preventDefault()
            let form = $('#register').serializeArray()
            let formData = objectifyForm(form)
            formData['username']=formData['email']

            console.log(formData)


            axios.post(auth_url, {...formData})
            .then(res => {
                console.log("succeeded")
                console.log(res)
                window.location.href = `http://127.0.0.1:8000/verify/register/`;
            })
            .catch(err => console.log(err))
        }
    )
})