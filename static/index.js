const form_reference=document.forms["contact_form_name"];
const apiUrl="https://script.google.com/macros/s/AKfycbxH6x7doosKyL8QWLJ5nWWBUG7H7t8PYDqh7R3ptY6FPjCHEeeQcy5GsJhXdayP8dgM/exec";

form_reference.addEventListener("submit",(event)=>{

    event.preventDefault();
    fetch(apiUrl,{
        method:"POST",
        body:new FormData(form_reference),
    })
    .then((response)=>{
        alert("You have submitted the form! I will get back to you shortly");
        document.getElementById("contact_form_id").reset();
    })
    .catch((error)=>{
        console.log(error)
    });
})
function formSubmit(){
 
}