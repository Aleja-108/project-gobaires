const btnAbrirModal = document.querySelector("#btn_abrir_modal");
const btnCerrarModal = document.querySelector("#btn_cerrar_modal");
const modal = document.querySelector("#form_resto");

btnAbrirModal.addEventListener("click", ()=>{
    modal.showModal();
})

btnCerrarModal.addEventListener("click", ()=>{
    modal.close();
})


 // Selecciona los elementos del formulario
 const formulario = document.getElementById('formulario_resto');
 const nombre = document.getElementById('nombre');
 const tel = document.getElementById('tel');
 const fecha = document.getElementById('fecha');
 const formDialog = document.getElementById('form_resto');
 const abrirFormularioBtn = document.getElementById('abrir_formulario');


 // Añade un evento al formulario para validar antes de enviar
 formulario.addEventListener('submit', function(event) {
     // Limpia cualquier mensaje de advertencia previo
     let warnings = '';
     let faltan_datos = false;

     // Valida el campo de nombre
     if (nombre.value.trim() === '') {
         warnings += 'Debe ingresar un nombre.\n';
         faltan_datos = true;
     }

     // Valida el campo de teléfono
     if (tel.value.trim() === '') {
         warnings += 'Debe ingresar un teléfono de contacto.\n';
         faltan_datos = true;
     } else if (!/^\d+$/.test(tel.value)) {
         warnings += 'El teléfono solo puede contener números.\n';
         faltan_datos = true;
     }

     // Valida el campo de fecha
     if (fecha.value.trim() === '') {
         warnings += 'Debe seleccionar una fecha.\n';
         faltan_datos = true;
     }

     // Si hay advertencias, evita el envío del formulario y muestra las advertencias
     if (faltan_datos) {
         alert(warnings);
         event.preventDefault();
     } else {
        // Si no hay advertencias, resetea el formulario
        formulario.reset();
        // Cierra el diálogo (opcional, si no se cierra automáticamente)
        formDialog.close();
    }
});



 