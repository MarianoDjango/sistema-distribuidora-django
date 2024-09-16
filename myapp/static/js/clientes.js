$(document).ready(function (){
  buscarcli();
});
function buscarcli(){
  var nombre = document.getElementById('clientesearch').value;
  var id_empresa = document.getElementById('idempresa').innerText;
  $('#clientesList').html("");
    $.ajax({
        url:'/myapp/clientes/',
        data:{
          id_empresa: id_empresa,
          nombre: nombre,
        },
        type:"get",
        datatype: "json",
        success:function(response){
          for(let i = 0;i < response.length;i++){
              $('#clientesList').append(response[i]['fila']);
          }
        },
      });
    }
