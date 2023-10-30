function passCheck()
{
    var first = document.getElementById("pswd");
    var second = document.getElementById("repeat-pswd");
    if (first.value != second.value)
    {
        alert("The passwords did not match. \n" + "Please re-enter your passwords carefully now.");
        return false;
    }
    else
    {
        return true;
    }
}