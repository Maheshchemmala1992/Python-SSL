

function priority_status_change(id) {
    var priority = $("#priority_" + id).val()
    var action = confirm("Are you sure to change the status...?")
    if (action == true) {
        $.ajax({
            type: "GET",
            url: "/",
            data: { 'id': id, 'priority': priority },
            success: function (data) {
                location.reload();
            },
            error: function (response) {
              
                location.reload();
            }
        });
    } else {
        id.preventDefault();
        location.reload();
    }
}


// function priority_status_modify(id) {
//     var priority = $("#modify_" + id).val()
//     var action = confirm("Are you sure to change the status...?")
//     if (action == true) {
//         $.ajax({
//             type: "GET",
//             url: "/",
//             data: { 'iss_id': id, 'issu_priority': priority },
//             success: function (data) {
//                 location.reload();
//             },
//             error: function (response) {
//                 alert('Error')
//                 location.reload();
//             }
//         });
//     } else {
//         id.preventDefault();
//         location.reload();
//     }
// }