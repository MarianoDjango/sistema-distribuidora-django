function familias_empresa(idempresa, nomempresa){
  var item = 'navi' + idempresa
  var nav = document.getElementById(item);
  nav.style.fontSize = 24
  $('navi' + idempresa).add("active");
  $('#empresa').html(nomempresa);
  $('#sidebar-nav').html("");
    $.ajax({
        url:'/myapp/familias/',
        data:{
          idempresa: idempresa,
        },
        type:"get",
        datatype: "json",
        success:function(response){
          for(let i = 0;i < response.length;i++){
              $('#sidebar-nav').append(response[i]['fila']);
          }
        },
      });
}
function buscart(){
  var nombre = document.getElementById('articsearch').value;
  var idfamilia = document.getElementById('idfamilia').innerText;
  var id_empresa = document.getElementById('idempresa').innerText;
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
