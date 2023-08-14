function user_user_measures() {
    var selectedOption = document.getElementById("options");
    var allDivs = document.querySelectorAll(".hidden");
    var hidden_file = document.getElementById("hidden_file");

    if (selectedOption.value == "u") {
        for (var i = 0; i < allDivs.length; i++) {
            allDivs[i].style.display = "block";
        }
    } 
    if (selectedOption.value == "c" || selectedOption.value == "a")
    {
        for (var i = 0; i < allDivs.length; i++) {
            allDivs[i].style.display = "none";
        }
    }

    if(selectedOption.value == "a")
    {
        hidden_file.style.display = "none";
    }
    else
    {
        hidden_file.style.display = "block";
    }
}
