function familias_empresa(idempresa, nomempresa){
  $('#navi' + idempresa).add("active");
  $('#empresa').html(nomempresa);
  $('#idempresa').html(idempresa);
  $('#sidebar-nav').html("");
    $.ajax({
        url:'/myapp/familias/',
        data:{
          idempresa: idempresa,
        },
        type:"get",
        datatype: "json",
        success:function(response){
          $('#idfamilia').html(response.id_familia)
          response.filas.forEach(function(item) {
            $('#sidebar-nav').append(item.fila);
          });
        },
      });
    buscart()
}

function buscart(){
  var nombre = document.getElementById('articsearch').value;
  var idfamilia = document.getElementById('idfamilia').innerHTML;
  var id_empresa = document.getElementById('idempresa').innerText;
  console.log(idfamilia)
  $('#articulosList').html("");
    $.ajax({
        url:'/myapp/articulos/',
        data:{
          nombre: nombre,
          familia: idfamilia,
          idempresa: id_empresa,
        },
        type:"get",
        datatype: "json",
        success:function(response){
          for(let i = 0;i < response.length;i++){
              $('#articulosList').append(response[i]['fila']);
          }
        },
      });
    }
