


function issue_status_change(id) {
    var issue_status = $("#issue_status_" + id).val()
    var action = confirm("Are you sure to change the status...?")
    if (action == true) {
        $.ajax({
            type: "GET",
            url: `/issue-status`,
            data: {'id': id, 'issue_status': issue_status},
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