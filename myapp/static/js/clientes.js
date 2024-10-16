$(document).ready(function (){
  buscarcli();
});
function buscarcli(){
  var nombre = document.getElementById('clientesearch').value;
  var id_empresa = document.getElementById('idempresa').innerText;
  var id_familia = document.getElementById('pfamilia').value;
  $('#clientesList').html("");
    $.ajax({
        url:'/myapp/clientes/?pfamilia=' + id_familia,
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
