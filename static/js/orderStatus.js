$("#cancelForm").submit(function(evt){
    evt.preventDefault();
    var con = confirm("Do you want to cancel this order?")
    if(con === true){
        $("#cancelForm").unbind("submit").submit();
    }
})


$("#returnForm").submit(function(evt){
    evt.preventDefault();
    var con = confirm("Do you want to return this order?")
    if(con === true){
        $("#returnForm").unbind("submit").submit();
    }
})