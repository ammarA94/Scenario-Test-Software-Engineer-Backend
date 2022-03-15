function SignUp() {
  try {
     if (!$("#file-upload-form")[0].checkValidity()) {
            $("#file-upload-form").find("#submit-hidden").click();
            return;
        } 
        else {
            swal("Please wait...", "", "success");
            $.ajax({
                type: 'POST',
                url: "/RegisterUser/",
                dataType: 'json',
                async: true,
                data:
                {
                    username: $('#username_id').val(),
                    email: $('#email_id').val(),
                    password: $('#password_id').val(),
                    'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
                },
                success: function (json) {
                    if(json.flag == true) {
                        $('#AuthenticationId').show()
                        $('#SignupId').hide()
                        $('#UpdatePasswordId').hide()
                        $('#email_id_AuthenticationProcess').val(json.email)
                        $('#AuthType_id').val(json.AuthType)           
                     }
                    else {
                        swal(json.Msg, "", "warning");
                    }
                }

            });
        }
        }
        catch (e) {
            swal(e, "", "warning");
        }
        
    }
    
function AuthenticationProcess() {
  try {
    if (!$("#form-action")[0].checkValidity()) {
           $("#form-action").find("#submit-hidden2").click();
           return;
       } 
       else {
           $.ajax({
               type: 'POST',
               url: "/AuthenticationProcess/",
               dataType: 'json',
               async: true,
               data:
               {
                   code: $('#code_id').val(),
                   email: $('#email_id_AuthenticationProcess').val(),
                   AuthType: $('#AuthType_id').val(),
                   'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
               },
               success: function (json) {
               console.log(json);
                if(json.flag == true &&  json.AuthType=='Forgot') {
                    $('#myModal').modal('hide');
                    $('#myModal2').modal('show');
                    $('#myModal3').modal('hide');
                }
                else if(json.flag == true &&  json.AuthType=='Register') {
                 swal({
                    title: "Success",
                    text: json.Msg,
                    icon: "success",
                    buttons: true,
                    dangerMode: true,
                })
                    .then((willDelete) => {
                        if (willDelete) {
                            window.location.href = "/login/";
                        } 
                        else{
                           window.location.href = "/login/";

                        }
                    });
                }

                   else {
                       swal(json.Msg, "", "warning");
                   }
               }

           });
       }
       }
       catch (e) {
           swal(e, "", "warning");
       }
       
   }
  
function Forgot_Password() {

  try {
    if (!$("#forgot-form")[0].checkValidity()) {
           $("#forgot-form").find("#submit-hidden2").click();
           return;
       } 
       else {
           swal("Please wait...", "", "success");
           $.ajax({
               type: 'POST',
               url: "/forgot_password/",
               dataType: 'json',
               async: true,
               data:
               {
                   forgot_email: $('#email_id_AuthenticationProcess').val(),
                   'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
               },
               success: function (json) {
               console.log(json);
                if(json.flag == true ) {
                    $('#myModal').modal('hide');
                    $('#myModal2').modal('hide');
                    $('#myModal3').modal('show');
                    $('#emailAuthId').val(json.email);
                }
                   else {
                       swal(json.Msg, "", "warning");
                   }
               }

           });
       }
       }
       catch (e) {
           swal(e, "", "warning");
       }
       
   } 
function UpdatePassword() {
    try {
        if (!$("#password-form")[0].checkValidity()) {
               $("#password-form").find("#submit-hidden_password").click();
               return;
           } 
        else {
          $.ajax({
              type: 'POST',
              url: "/UpdatePassword/",
              dataType: 'json',
              async: true,
              data:
              {
                  email: $('#email_id_AuthenticationProcess').val(),
                  password: $('#update_password_id').val(),
                  'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
              },
              success: function (json) {
                if(json.flag == true) {
                      $('#myModal').modal('hide');
                      $('#myModal2').modal('hide');
                      $('#myModal3').modal('hide');
                      swal(json.Msg, "", "success");
                  }
                  else {
                      swal(json.Msg, "", "warning");
                  }
              }

          });
      }
      }
      catch (e) {
          swal(e, "", "warning");
      }
      
  }
function Login() {
  try {
   if (!$("#form-action_login")[0].checkValidity()) {
            $("#form-action_login").find("#submit-hidden_login").click();
            return;
        } 
        else {
            $.ajax({
                type: 'POST',
                url: "login_authentication/",
                dataType: 'json',
                async: true,
                data:
                {
                    email: $('#emailId').val(),
                    password: $('#passwordId').val(),
                    'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
                },
                success: function (json) {
                    if(json.flag == true) {
                        window.location.href = "/YourApps/";
                    }

                    else {
                        swal(json.Msg, "", "warning");
                    }
                }

            });
        }
        }
        catch (e) {
            swal(e, "", "warning");
        }
        
    }
    
function LogOut() {
  try {
   
            $.ajax({
                type: 'POST',
                url: "/logout/",
                dataType: 'json',
                async: true,
                data:
                {
                    'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
                },
                success: function (json) {
                        window.location.href = "/login/";
                }

            });
        }
        catch (e) {
            swal(e, "", "warning");
        }
        }

function CreateApp() {
  try {
        if (!$("#file-upload-form")[0].checkValidity()) {
                 $("#file-upload-form").find("#submit-hidden").click();
                 return;
        } 
        else {
            $.ajax({
                type: 'POST',
                url: "/SaveApps/",
                dataType: 'json',
                async: true,
                data:
                {
                    app_name: $('#app_id').val(),
                    description: $('#description_id').val(),
                    'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
                },
                success: function (json) {
                    if(json.flag == true) {
                     swal({
                    title: "Success",
                    text: json.Msg,
                    icon: "success",
                    buttons: true,
                    dangerMode: true,
                })
                    .then((willDelete) => {
                        if (willDelete) {
                            window.location.href = "/YourApps/";
                        } 
                    });
                    }
                    else {
                        swal(json.Msg, "", "warning");
                    }
                }

            });
        }
        }
        catch (e) {
            swal(e, "", "warning");
        }
        
    }
    
 function show_detail(id) {
         $.ajax({
                type: 'POST',
                url: "/detail_app/",
                dataType: 'json',
                async: true,
                data:
                {
                    app_id:id,
                    'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
                },
                success: function (json) {
                    if(json.flag == true) {
                        $('#mymodal_div').text(json.Data[2]);
                        $('#exampleModal').modal('show');
                    }
                }

            });

    }
    
 function show_update_form() {
    var check_value = $('.selected_id:checked').val();
    if (!check_value) {
        swal("Select an App first.", "", "warning");
        return;
         } 
    $.ajax({
       type: 'POST',
       url: "/detail_app/",
       dataType: 'json',
       async: true,
       data:
       {
           app_id:check_value,
           'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
       },
       success: function (json) {
           if(json.flag == true) {
               $('#myModalUpdate').modal('show');
               $('#app_id').val(json.Data[1]);
               $("#SubscriptionId").val(json.Data[3]).change();
               $('#description_id').text(json.Data[2]);

           }
       }

   });

    }
 function SaveUpdatedApp() {
    try {
        var check_value = $('.selected_id:checked').val();
        if (!check_value) {
            swal("Select an App first.", "", "warning");
            return;
         } 
            else {
               $.ajax({
               type: 'POST',
               url: "/SaveUpdatedApp/",
               dataType: 'json',
               async: true,
               data:
               {
                    app_id: check_value,
                    app_name: $('#app_id').val(),
                    description: $('#description_id').val(),
                    SubscriptionId: $('#SubscriptionId').val(),
                    'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
                    },
                    success: function (json) {
                    if(json.flag == true) {
                       swal({
                       title: "Success",
                       text: json.Msg,
                       icon: "success",
                       buttons: true,
                       dangerMode: true,
                            })
                       .then((willDelete) => {
                               window.location.href = "/YourApps/";
                           
                       }); 
                       }
                   else {
                       swal(json.Msg, "", "warning");
                   }
                    }
    
                });
             }
             }
             catch (e) {
                 swal(e, "", "warning");
             }
             
    }
    
function DeleteApp() {
    var check_value = $('.selected_id:checked').val();
    if (!check_value) {
        swal("Select an App first.", "", "warning");
        return;
         } 
        swal({
            title: "Delete",
            text: "Are you sure?",
            icon: "warning",
            buttons: true,
            dangerMode: true,
        })
            .then((willDelete) => {
                if (willDelete) {
                    $.ajax({
       type: 'POST',
       url: "/delete_app/",
       dataType: 'json',
       async: true,
       data:
       {
           app_id:check_value,
           'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
       },
       success: function (json) {
           if(json.flag == true) {
                swal({
                title: "Success",
                text: json.Msg,
                icon: "success",
                buttons: true,
                dangerMode: true,
                     })
                .then((willDelete) => {
                        window.location.href = "/YourApps/";
                    
                }); 
                }
            else {
                swal(json.Msg, "", "warning");
                   }
                }
         
            });
                } else {
                }
            });
        }


function CancelSubscription() {
    var check_value = $('.selected_id:checked').val();
    if (!check_value) {
        swal("Select an App first.", "", "warning");
        return;
         } 
        swal({
            title: "Cancel",
            text: "Are you sure to cancel your subscription?",
            icon: "warning",
            buttons: true,
            dangerMode: true,
        })
            .then((willDelete) => {
                if (willDelete) {
                    $.ajax({
       type: 'POST',
       url: "/cancelsubscription/",
       dataType: 'json',
       async: true,
       data:
       {
           app_id:check_value,
           'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
       },
       success: function (json) {
           if(json.flag == true) {
                swal({
                title: "Success",
                text: json.Msg,
                icon: "success",
                buttons: true,
                dangerMode: true,
                     })
                .then((willDelete) => {
                        window.location.href = "/YourApps/";
                    
                }); 
                }
            else {
                swal(json.Msg, "", "warning");
                   }
                }
         
            });
                } else {
                }
            });
        }

