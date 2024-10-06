//Aparece el Botón de Volver Arriba
let mybutton = document.getElementById("Top");

//El botón aparecerá al hacer un scroll de 20px desde el top del documento.
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        mybutton.style.display = "block";
    } else {
        mybutton.style.display = "none";
    }
}

//Cuando el usuario hace clic en el botón, se desplaza hacia la parte superior del documento
function topFunction() {
    document.body.scrollTop = 0; // Para Safari
    document.documentElement.scrollTop = 0; // Para Chrome, Firefox, IE y Opera
}
