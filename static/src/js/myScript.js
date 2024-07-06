    /** @odoo-module **/
import publicWidget from '@web/legacy/js/public/public_widget';

console.log('working......')
publicWidget.registry.websiteEvents = publicWidget.Widget.extend({
    selector: '.form_validate',
    events: {
        'change .phone': '_phone',
        'change .aadhar': '_aadhar',
        'change .calculate_age': '_calculate_age',
        'click .submit_btn': '_submit_btn',
    },
    _phone: function (ev) {
        let phone_error = true
        let phone = document.getElementById("phone").value;
        if (phone.length != 10){
            console.log("phone number should 10")
            document.getElementById("phonemessage").innerHTML = "Phone Number should be 10 digit";
            phone_error = false
            return false
        }
        if ($.isNumeric(phone) == false){
            console.log("phone number should numeric")
            document.getElementById("phonemessage").innerHTML = "Phone Number should be Numeric";
            phone_error = false
            return false
        }
        if (phone.length == 10){
            document.getElementById("phonemessage").innerHTML = "";
            phone_error = true
            return true
        }
    },
    _aadhar: function (ev) {
        let aadhar_error = true;
        let aadhar = document.getElementById("aadhar").value;
        if (aadhar.length != 12)
        {
        document.getElementById("adharmessage").innerHTML = "Aadhar Number should be 12 digit";
        console.log("Aadhar number should 12")
        aadhar_error = false;
        return false
        }
        if ($.isNumeric(aadhar) == false){
        document.getElementById("adharmessage").innerHTML = "Aadhar Number should be Numeric";
        console.log("Aadhar number should numeric")
        aadhar_error = false;
        return false
        }
        if (aadhar.length == 12)
        {
        document.getElementById("adharmessage").innerHTML = "";
        aadhar_error = true;
        return true
        }
    },
    _calculate_age: function (ev) {
        let age_error = false;
        let dob = new Date($("#dob").val());
        let today = new Date()
        let age = today.getFullYear() - dob.getFullYear();
        console.log(age)
        if (age < 18){
            document.getElementById("agemessage").innerHTML = "Age should greater than 18";
            document.getElementById("age").value = 0;
            age_error = false
            return false
        }
        else{
            document.getElementById("age").value = age;
            document.getElementById("agemessage").innerHTML = "";
            age_error = true
            return true
        }
    },
    _submit_btn: function (ev){

       console.log(this._aadhar())
       console.log(this._calculate_age())
       console.log(this._phone())
       if (this._aadhar() == true && this._calculate_age() == true && this._phone() == true ){
            console.log("correct")
            window.alert("success fully registered")
       }
        else{
            window.alert("Check your data")
        }

    }
});
