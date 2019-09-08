function display_sw2(msg, type) {
  Swal.fire({
      type: type,
      title: 'Update',
      text: msg,
  })
}

function update(url) {
    myXHR = $.ajax({
    url: url,
    complete: function (xhr, statusText) {
      if (xhr.status == 200) {
        console.log(statusText);
        response = JSON.parse(myXHR.responseText);
        console.log(response);
        message = response["message"];
        display_sw2(message, 'success');
      }
    }
  });
}


function action(url, data) {
    myXHR = $.ajax({
    url: url,
    type:"POST",
    dataType: "json",
    data: JSON.parse(data),
    complete: function (xhr, statusText) {
      if (xhr.status != 200) {
        message = url + " received an unexpected request.";
        display_sw2(message, 'error');
      }
      else {
        message = "Your request has been successfully registered. You will be notified when it is done.";
        display_sw2(message, 'success');
      }
    }
  });
}


function show_config(config){
      Swal.fire({
          type: 'info',
          title: 'Config',
          html: config,
      });
}


function remove_vlan(url, vlan_num) {
    Swal.fire({
      title: 'Are you sure?',
      text: "You won't be able to revert this!",
      type: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
      if (result.value) {
        action(url, "{\"type\": \"remove\", \"vlan_number\": \""+vlan_num+"\"}")
      }
    })
}


function add_vlan(url) {
    Swal.mixin({
      input: 'text',
      confirmButtonText: 'Next &rarr;',
      showCancelButton: true,
      progressSteps: ['1', '2']
    }).queue([
      {
        title: 'Choose VLAN id',
        text: 'The selected id needs to be > 121'
      },
      {
        title: 'Choose VLAN subnet',
        text: 'The selected subnet should be writen as A.B.C.D/E'
      }
    ]).then((result) => {
      if (result.value) {
        action(url, "{\"type\": \"add\", \"vlan_number\": \""+result.value[0]+"\", \"subnet\": \""+result.value[1]+"\"}")
      }
    })
}
