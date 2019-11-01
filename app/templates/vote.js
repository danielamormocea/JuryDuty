function dlgCancel(){
    dlgHide();
    }
    function dlgOK(){
        dlgHide();
    }
    function dlgHide(){
        var whitebg = document.getElementById("white-background");
        var dlg = document.getElementById("dlgbox");
        whitebg.style.display = "none";
        dlg.style.display = "none";
    }
    function showDialog(current_user){
        if (current_user.type_user !== 3) {
            var whitebg = document.getElementById("white-background");
            var dlg = document.getElementById("dlgbox");
            whitebg.style.display = "block";
            dlg.style.display = "block";
            var winWidth = window.innerWidth;
            dlg.style.left = (winWidth / 2) - 480 / 2 + "px";
            dlg.style.top = "150px";
        }
    }