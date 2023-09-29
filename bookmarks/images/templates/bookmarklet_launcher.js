/*
Este script descubre si el bookmarklet ya fue cargado verificando
la variable myBookMarklet, si esta definida o no.
Al haer eso se evitar cargarlo nuevamente en caso el usuario clique
en el bookmarklet repetidamente.
Si el bookmarklet esta definido, carga otro archivo js agregando un
elemento <script> en el documento.
La tag script carga el bookmarklet.js usando un numero aletaorio como
parámetro para evitar que el archivo sea cargado del cache del navegador

*/
(function(){
    if (window.myBookmarklet !== undefined){
        myBookmarklet();
    }
    else {
        document.body.appendChild(document.createElement('script')).src='https://localhost:8000/static/js/bookmarklet.js?r='+Math.floor(Math.random()*99999999999999999999);
    }
})();