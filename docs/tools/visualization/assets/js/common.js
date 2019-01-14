//入力フォーム関連の処理
function file_input(){
  var file = $('#getfile')[0]
  file.onchange = function ()
  {
    const fileList = file.files
    var reader = new FileReader()
    reader.readAsText(fileList[0])

    reader.onload = function ()
    {
      showxml(reader.result, true)

    }
  }
}

function getParam(){
  var vars = {};
  var param = location.search.substring(1).split('&');
  for(var i = 0; i < param.length; i++) {
    var keySearch = param[i].search(/=/);
    var key = '';
    if(keySearch != -1) key = param[i].slice(0, keySearch);
    var val = param[i].slice(param[i].indexOf('=', 0) + 1);
    if(key != '') vars[key] = decodeURI(val);
  }
  return vars;
}
